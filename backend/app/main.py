import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base, AsyncSessionLocal
from app.services.seed_demo import seed_demo_data

from app.routers import dashboard, projects, characters, stories, scenes, voice, assembly

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed demo data (The Village of Shadows)
    async with AsyncSessionLocal() as session:
        await seed_demo_data(session)

    yield

app = FastAPI(
    title="AI Cartoon Studio API",
    description="Automated 3D Animated Cartoon Production Engine",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated media assets
app.mount("/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")

# Include Routers
app.include_router(dashboard.router)
app.include_router(projects.router)
app.include_router(characters.router)
app.include_router(stories.router)
app.include_router(scenes.router)
app.include_router(voice.router)
app.include_router(assembly.router)

@app.get("/api/health")
async def health_check():
    return {
        "status": "online",
        "service": "AI Cartoon Studio Backend",
        "version": "1.0.0"
    }
