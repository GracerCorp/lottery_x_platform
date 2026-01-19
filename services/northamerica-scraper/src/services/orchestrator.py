"""Scraper orchestration logic"""

from src.scrapers import get_scraper_by_slug
from src.utils.logger import get_logger

logger = get_logger(__name__)


def run_scraper(slug: str) -> dict:
    """
    Execute a scraper by its slug
    
    Args:
        slug: Lottery slug
    
    Returns:
        Dict with execution summary
    """
    logger.info("Running scraper", slug=slug)
    
    try:
        scraper = get_scraper_by_slug(slug)
        if not scraper:
            error_msg = f"No scraper found for slug: {slug}"
            logger.error(error_msg)
            return {"status": "failed", "error": error_msg}
        
        result = scraper.run()
        return result
        
    except Exception as e:
        logger.error("Scraper execution failed", slug=slug, error=str(e), exc_info=True)
        return {
            "status": "failed",
            "slug": slug,
            "error": str(e)
        }
