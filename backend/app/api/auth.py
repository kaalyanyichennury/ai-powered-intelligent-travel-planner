import hashlib
import re
import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..database.models import AuthSessionModel, UserModel

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class SignInRequest(BaseModel):
    email: str
    password: str


class AuthUser(BaseModel):
    id: int
    email: str


class SignInResponse(BaseModel):
    token: str
    user: AuthUser


def _hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000,
    ).hex()


def _create_session(db: Session, user: UserModel) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=7)
    db.add(AuthSessionModel(user_id=user.id, token=token, expires_at=expires_at))
    db.commit()
    return token


def _is_valid_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email))


@router.post("/signin", response_model=SignInResponse)
def sign_in(request: SignInRequest, db: Session = Depends(get_db)):
    email = request.email.strip().lower()
    password = request.password.strip()

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required.",
        )

    if not _is_valid_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a valid email address.",
        )

    user = db.query(UserModel).filter(UserModel.email == email).first()

    if user is None:
        salt = secrets.token_hex(16)
        user = UserModel(
            email=email,
            password_hash=_hash_password(password, salt),
            password_salt=salt,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        expected_hash = _hash_password(password, user.password_salt)
        if not secrets.compare_digest(expected_hash, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

    token = _create_session(db, user)
    return {"token": token, "user": {"id": user.id, "email": user.email}}


@router.get("/me")
def get_current_user(
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    token = authorization.split(" ", 1)[1].strip()
    session = db.query(AuthSessionModel).filter(AuthSessionModel.token == token).first()

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session.",
        )

    if session.expires_at <= datetime.utcnow():
        db.delete(session)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired.",
        )

    user = db.query(UserModel).filter(UserModel.id == session.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists.",
        )

    return {"id": user.id, "email": user.email}
