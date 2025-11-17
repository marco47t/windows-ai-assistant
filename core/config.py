"""Configuration management."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings."""
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Provider Configuration
    DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "auto")
    ROUTING_TOKEN_THRESHOLD: int = int(os.getenv("ROUTING_TOKEN_THRESHOLD", "1000"))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    
    # Model Configuration
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///data/assistant.db")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/assistant.log")
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    def __init__(self):
        """Initialize settings and create directories."""
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)
    
    def validate(self):
        """Validate required settings."""
        if not self.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required. Please set it in .env file.")


settings = Settings()