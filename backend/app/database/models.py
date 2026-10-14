import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from .database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    password_salt = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AuthSessionModel(Base):
    __tablename__ = "auth_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

class TripModel(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(String(64), unique=True, index=True)
    title = Column(String(255), nullable=False)
    destination = Column(String(128), index=True)
    country = Column(String(128), nullable=True)
    duration_days = Column(Integer, default=7)
    travelers = Column(Integer, default=2)
    budget = Column(Float, default=2500.0)
    currency = Column(String(10), default="USD")
    plan_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AnalyticsLogModel(Base):
    __tablename__ = "analytics_logs"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String(128), index=True)
    duration_days = Column(Integer, default=7)
    budget_usd = Column(Float, default=2500.0)
    currency = Column(String(10), default="USD")
    interests_str = Column(String(255))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
