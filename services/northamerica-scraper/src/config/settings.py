"""Application settings using Pydantic"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://lottery_user:lottery_pass@localhost:5432/lottery_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API
    API_SECRET_KEY: str = "change-me-in-production"
    API_PORT: int = 8001
    
    # Selenium
    SELENIUM_HEADLESS: bool = True
    SELENIUM_TIMEOUT: int = 30
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_PERIOD: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Sentry
    SENTRY_DSN: str = ""
    
    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
