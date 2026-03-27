"""
Notevera AI – Main FastAPI Application
Run with: uvicorn app:app --reload --port 8000
"""
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Add backend dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from database import database, metadata, engine
from routes import auth, upload, notes, planner, oral_exam, profile, settings, export


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    metadata.create_all(engine)
    await database.connect()
    print("✅ Database connected & tables created")
    yield
    await database.disconnect()
    print("🔌 Database disconnected")


app = FastAPI(
    title="Notevera AI API",
    description="AI-powered smart learning assistant backend",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(notes.router)
app.include_router(planner.router)
app.include_router(oral_exam.router)
app.include_router(profile.router)
app.include_router(settings.router)
app.include_router(export.router)


@app.get("/")
async def root():
    return {
        "name": "Notevera AI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
