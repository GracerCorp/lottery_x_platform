"""Scraper registry for North America lotteries"""

from src.scrapers.countries.usa import PowerballScraper, MegaMillionsScraper
from src.scrapers.countries.canada import Lotto649Scraper, LottoMaxScraper
from src.scrapers.countries.mexico import MelateScraper, ChispazoScraper

# Registry mapping slug to scraper class
SCRAPER_REGISTRY = {
    # United States
    "us-powerball": PowerballScraper,
    "us-megamillions": MegaMillionsScraper,
    
    # Canada
    "ca-lotto649": Lotto649Scraper,
    "ca-lottomax": LottoMaxScraper,
    
    # Mexico
    "mx-melate": MelateScraper,
    "mx-chispazo": ChispazoScraper,
    
    # Note: Other countries can be added as scrapers are implemented
    # For now, unimplemented scrapers will return None
}


def get_scraper_by_slug(slug: str):
    """
    Get scraper instance by lottery slug
    
    Args:
        slug: Lottery slug (e.g., 'us-powerball')
    
    Returns:
        Scraper instance or None if not found
    """
    scraper_class = SCRAPER_REGISTRY.get(slug)
    if scraper_class:
        return scraper_class(slug)
    return None
