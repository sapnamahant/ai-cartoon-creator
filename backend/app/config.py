import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite+aiosqlite:///./studio.db"
    
    # API Keys
    GEMINI_API_KEY: str = ""
    ELEVENLABS_API_KEY: str = ""
    KLING_API_KEY: str = ""
    REPLICATE_API_TOKEN: str = ""
    
    # Fallback to smart simulated/mock generation when keys are absent
    ALLOW_MOCK_FALLBACK: bool = True
    
    MEDIA_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage")
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
os.makedirs(settings.MEDIA_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.MEDIA_DIR, "images"), exist_ok=True)
os.makedirs(os.path.join(settings.MEDIA_DIR, "videos"), exist_ok=True)
os.makedirs(os.path.join(settings.MEDIA_DIR, "audio"), exist_ok=True)
os.makedirs(os.path.join(settings.MEDIA_DIR, "exports"), exist_ok=True)
