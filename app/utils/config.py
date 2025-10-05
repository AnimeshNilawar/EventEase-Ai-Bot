# app/utils/config.py
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DEBUG: bool = True
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    DATA_DIR: str = "data"
    VECTOR_DIR: str = "data/vector_store"
    CHUNK_SIZE: int = 1000        # characters per chunk (simple splitter)
    CHUNK_OVERLAP: int = 200

    # Enforce Gradient Serverless only for chat + embeddings
    USE_GRADIENT: bool = True
    GRADIENT_API_KEY: str | None = None
    GRADIENT_API_BASE: str = "https://inference.do-ai.run"
    GRADIENT_MODEL: str = "gpt-4o-mini"

    # Embeddings via Gradient only
    USE_GRADIENT_EMBEDDINGS: bool = True
    # Set to a valid Gradient embeddings model; must be provided in .env
    GRADIENT_EMBEDDING_MODEL: str | None = None

    # Keep placeholders for OpenAI keys but they are unused now
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str | None = None
    OPENAI_EMBEDDING_MODEL: str | None = None

    # Local ST model name retained but not used when Gradient is enabled
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_BATCH_SIZE: int = 32

    class Config:
        env_file = ".env"

settings = Settings()
