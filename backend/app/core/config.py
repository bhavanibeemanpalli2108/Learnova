from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from .env
    """

    # Application
    APP_NAME: str = "AI-Powered Study Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Gemini
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.5-flash"

    # Voyage AI
    VOYAGE_API_KEY: str
    EMBEDDING_MODEL: str = "voyage-3-large"

    # Qdrant
    QDRANT_URL: str
    QDRANT_API_KEY: str
    QDRANT_COLLECTION: str = "study_documents"

    # LangSmith
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str = "AI-Study-Assistant"
    LANGSMITH_TRACING: bool = True
    LANGSMITH_ENDPOINT: str

    # Upload Configuration
    UPLOAD_DIRECTORY: str = "uploads"

    MAX_FILE_SIZE_MB: int = 50

    TAVILY_API_KEY: str

    # Chunking
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # API
    API_PREFIX: str = "/api/v1"

    #BackEndURL
    # BACKEND_URL = "http://127.0.0.1:8000/api/v1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()