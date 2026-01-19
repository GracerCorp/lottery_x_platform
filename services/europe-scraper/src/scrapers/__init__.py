"""Scraper registry for all European countries"""

from src.scrapers.countries.uk import UKNationalLotteryScraper, UKThunderballScraper
from src.scrapers.countries.spain import SpainPrimitivaScraper

# Scraper registry mapping slug -> scraper class
SCRAPER_REGISTRY = {
    # United Kingdom
    "uk-national-lottery": UKNationalLotteryScraper,
    "uk-thunderball": UKThunderballScraper,
    
    # Spain
    "es-primitiva": SpainPrimitivaScraper,
    
    # TODO: Add more country scrapers as they are implemented
    # Pan-European
    # "eu-euromillions": EuroMillionsScraper,
    # "eu-eurojackpot": EuroJackpotScraper,
    
    # France
    # "fr-loto": FranceLotoScraper,
    
    # Italy
    # "it-superenalotto": ItalySuperEnalottoScraper,
    # "it-million-day": ItalyMillionDayScraper,
    
    # Germany
    # "de-lotto-6aus49": GermanyLotto6aus49Scraper,
    
    # And so on for other countries...
}


def get_scraper_by_slug(slug: str):
    """Get scraper instance by slug"""
    scraper_class = SCRAPER_REGISTRY.get(slug)
    if scraper_class:
        return scraper_class(slug)
    return None


def get_all_scraper_slugs():
    """Get all registered scraper slugs"""
    return list(SCRAPER_REGISTRY.keys())
