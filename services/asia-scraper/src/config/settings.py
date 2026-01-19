from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment"""
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Application
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    MAX_CONCURRENT_SCRAPERS: int = 3
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_SECRET_KEY: str
    
    # Scraper
    DEFAULT_TIMEOUT: int = 30
    DEFAULT_RETRIES: int = 3
    SCRAPER_USER_AGENT: str = "Mozilla/5.0 (compatible; AsiaLotteryBot/1.0)"
    
    # Selenium
    CHROME_DRIVER_PATH: str = "/usr/bin/chromedriver"
    HEADLESS_MODE: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
