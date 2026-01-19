import pytest
from src.scrapers import get_scraper_by_slug, get_all_scraper_slugs, SCRAPER_REGISTRY


def test_scraper_registry_completeness():
    """Test that all expected scrapers are registered"""
    expected_slugs = [
        "in-kerala-lottery", "in-sikkim-lottery",
        "sg-toto", "sg-4d",
        "my-magnum-4d", "my-sports-toto",
        "th-government-lottery",
        "ph-pcso-lotto",
        "jp-takarakuji",
        "kr-lotto-645",
        "tw-welfare-lottery",
        "hk-mark-six",
        "vn-vietlott"
    ]
    
    registered_slugs = get_all_scraper_slugs()
    
    for slug in expected_slugs:
        assert slug in registered_slugs, f"Missing scraper: {slug}"
    
    assert len(registered_slugs) == 13


def test_get_scraper_by_slug():
    """Test getting scrapers by slug"""
    # Valid slugs
    kerala_scraper = get_scraper_by_slug("in-kerala-lottery")
    assert kerala_scraper is not None
    assert kerala_scraper.name == "Kerala State Lottery"
    
    toto_scraper = get_scraper_by_slug("sg-toto")
    assert toto_scraper is not None
    assert toto_scraper.name == "Singapore TOTO"
    
    # Invalid slug
    invalid_scraper = get_scraper_by_slug("invalid-slug")
    assert invalid_scraper is None


def test_all_scrapers_have_required_config():
    """Test that all scrapers have required configuration"""
    for slug, scraper_class in SCRAPER_REGISTRY.items():
        scraper = scraper_class()
        
        # Check required attributes
        assert hasattr(scraper, 'name'), f"{slug} missing name"
        assert hasattr(scraper, 'url'), f"{slug} missing url"
        assert hasattr(scraper, 'config'), f"{slug} missing config"
        
        # Check config has schedule
        assert 'schedule' in scraper.config, f"{slug} missing schedule in config"
        
        # Check URL is valid
        assert scraper.url.startswith('http'), f"{slug} has invalid URL"


@pytest.mark.asyncio
async def test_all_scrapers_implement_scrape():
    """Test that all scrapers implement the scrape method"""
    for slug, scraper_class in SCRAPER_REGISTRY.items():
        scraper = scraper_class()
        
        # Check method exists
        assert hasattr(scraper, 'scrape'), f"{slug} missing scrape method"
        assert callable(scraper.scrape), f"{slug} scrape is not callable"
