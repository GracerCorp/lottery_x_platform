import asyncio
import sys
from src.database.session import init_db
from src.services.scheduler import start_scheduler, schedule_scraper, stop_scheduler
from src.config.countries import ASIAN_COUNTRIES
from src.utils.logger import get_logger
from src.api.main import app
import uvicorn

logger = get_logger(__name__)


def init_database():
    """Initialize database and create tables"""
    logger.info("Initializing database")
    init_db()
    logger.info("Database initialized")


def load_scrapers():
    """Load and schedule all scrapers from config"""
    logger.info("Loading scrapers")
    
    for country in ASIAN_COUNTRIES:
        for lottery in country.lotteries:
            slug = lottery['slug']
            cron = lottery['schedule']
            
            try:
                schedule_scraper(slug, cron)
                logger.info(f"Loaded scraper", slug=slug, cron=cron)
            except Exception as e:
                logger.error(f"Failed to load scraper", slug=slug, error=str(e))


def start_api_server():
    """Start FastAPI server"""
    logger.info("Starting API server", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


def main():
    """Main entry point"""
    logger.info("=== Asia Lottery Scraper Starting ===")
    
    try:
        # Initialize database
        init_database()
        
        # Start scheduler
        start_scheduler()
        
        # Load all scrapers
        load_scrapers()
        
        # Start API server (blocking)
        start_api_server()
        
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        stop_scheduler()
        sys.exit(0)
    except Exception as e:
        logger.error("Fatal error", error=str(e), exc_info=True)
        stop_scheduler()
        sys.exit(1)


if __name__ == "__main__":
    main()
