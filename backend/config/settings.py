"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Intelligent Document Automation System"
    DEBUG: bool = True
    
    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "document_automation"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Storage settings
    STORAGE_TYPE: str = "local"  # local, s3, minio
    STORAGE_PATH: str = "./storage"
    
    # OCR settings
    TESSERACT_PATH: str = "/usr/bin/tesseract"
    
    # Elasticsearch settings
    ELASTICSEARCH_HOST: str = "localhost"
    ELASTICSEARCH_PORT: int = 9200
    
    # AI Model settings
    HUGGINGFACE_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    OPENAI_API_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
