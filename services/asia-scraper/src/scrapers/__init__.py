"""Scraper registry for all Asian countries"""

from src.scrapers.countries.india import IndiaKeralaLotteryScraper, IndiaSikkimLotteryScraper
from src.scrapers.countries.singapore import SingaporeTOTOScraper, Singapore4DScraper
from src.scrapers.countries.malaysia import MalaysiaMagnum4DScraper, MalaysiaSportsTOTOScraper
from src.scrapers.countries.thailand import ThailandGovernmentLotteryScraper
from src.scrapers.countries.philippines import PhilippinesPCSOLottoScraper
from src.scrapers.countries.japan import JapanTakarakujiScraper
from src.scrapers.countries.south_korea import SouthKoreaLotto645Scraper
from src.scrapers.countries.taiwan import TaiwanWelfareLotteryScraper
from src.scrapers.countries.hong_kong import HongKongMarkSixScraper
from src.scrapers.countries.vietnam import VietnamVietlottScraper

# Scraper registry mapping slug -> scraper class
SCRAPER_REGISTRY = {
    # India
    "in-kerala-lottery": IndiaKeralaLotteryScraper,
    "in-sikkim-lottery": IndiaSikkimLotteryScraper,
    
    # Singapore
    "sg-toto": SingaporeTOTOScraper,
    "sg-4d": Singapore4DScraper,
    
    # Malaysia
    "my-magnum-4d": MalaysiaMagnum4DScraper,
    "my-sports-toto": MalaysiaSportsTOTOScraper,
    
    # Thailand
    "th-government-lottery": ThailandGovernmentLotteryScraper,
    
    # Philippines
    "ph-pcso-lotto": PhilippinesPCSOLottoScraper,
    
    # Japan
    "jp-takarakuji": JapanTakarakujiScraper,
    
    # South Korea
    "kr-lotto-645": SouthKoreaLotto645Scraper,
    
    # Taiwan
    "tw-welfare-lottery": TaiwanWelfareLotteryScraper,
    
    # Hong Kong
    "hk-mark-six": HongKongMarkSixScraper,
    
    # Vietnam
    "vn-vietlott": VietnamVietlottScraper,
}


def get_scraper_by_slug(slug: str):
    """Get scraper instance by slug"""
    scraper_class = SCRAPER_REGISTRY.get(slug)
    if scraper_class:
        return scraper_class()
    return None


def get_all_scraper_slugs():
    """Get all registered scraper slugs"""
    return list(SCRAPER_REGISTRY.keys())
