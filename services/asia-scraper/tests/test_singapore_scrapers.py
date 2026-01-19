import pytest
from datetime import date
from src.scrapers.countries.singapore import SingaporeTOTOScraper, Singapore4DScraper


@pytest.mark.asyncio
async def test_toto_scraper_initialization():
    """Test TOTO scraper initializes correctly"""
    scraper = SingaporeTOTOScraper()
    
    assert scraper.name == "Singapore TOTO"
    assert "singaporepools.com.sg" in scraper.url
    assert scraper.config['schedule'] == "0 19 * * 1,4"  # Mon, Thu


@pytest.mark.asyncio
async def test_4d_scraper_initialization():
    """Test 4D scraper initializes correctly"""
    scraper = Singapore4DScraper()
    
    assert scraper.name == "Singapore 4D"
    assert "singaporepools.com.sg" in scraper.url
    assert scraper.config['schedule'] == "0 19 * * 3,6,0"  # Wed, Sat, Sun


@pytest.mark.asyncio
async def test_toto_result_structure():
    """Test TOTO result has correct structure"""
    from src.scrapers.base.base_scraper import ScrapedResult
    
    # TOTO draws 6 numbers + 1 additional
    result = ScrapedResult(
        draw_date=date(2026, 1, 19),
        winning_numbers=[3, 12, 18, 25, 34, 42],
        bonus_numbers=[7],
        jackpot={"amount": 2000000, "currency": "SGD"},
        raw_data={"source": "toto"}
    )
    
    assert len(result.winning_numbers) == 6
    assert len(result.bonus_numbers) == 1
    assert result.jackpot['currency'] == "SGD"
