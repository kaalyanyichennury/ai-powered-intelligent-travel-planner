import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from .database.database import engine, Base
from .database import models
from .api import travel, recommendation, chat, weather, analytics, auth
from .services.currency_service import currency_service
from .services.gemini_service import GeminiError, gemini_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("TravelPlannerApp")

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Intelligent Travel Planner API",
    description="Worldwide Agentic AI Travel Planning Platform with ML Recommender, RAG, and Real-time APIs",
    version="2.0.0"
)

@app.exception_handler(GeminiError)
async def handle_gemini_error(_, exc: GeminiError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc)},
    )

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(travel.router)
app.include_router(recommendation.router)
app.include_router(chat.router)
app.include_router(weather.router)
app.include_router(analytics.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Initializing AI Travel Planner backend services...")
    if gemini_service.is_configured:
        logger.info("Gemini LLM enabled with model %s.", gemini_service.model)
    else:
        logger.warning("Gemini LLM is not configured; local NLP and RAG fallbacks are active.")
    currency_service.refresh_rates()
    logger.info("AI Travel Planner backend is ready!")

@app.get("/")
def root():
    return {
        "status": "healthy",
        "app": "AI-Powered Intelligent Travel Planner",
        "version": "2.0.0",
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI Travel Planner services operational",
        "llm": {
            "provider": "Google Gemini",
            "model": gemini_service.model,
            "configured": gemini_service.is_configured,
        },
    }
