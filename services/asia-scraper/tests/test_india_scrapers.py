import pytest
from datetime import date
from src.scrapers.countries.india import IndiaKeralaLotteryScraper, IndiaSikkimLotteryScraper


@pytest.mark.asyncio
async def test_kerala_scraper_initialization():
    """Test Kerala scraper initializes correctly"""
    scraper = IndiaKeralaLotteryScraper()
    
    assert scraper.name == "Kerala State Lottery"
    assert scraper.url == "https://www.keralalotteryresult.net/"
    assert scraper.config['schedule'] == "0 16 * * *"


@pytest.mark.asyncio
async def test_kerala_scraper_validation():
    """Test Kerala scraper validation logic"""
    scraper = IndiaKeralaLotteryScraper()
    
    from src.scrapers.base.base_scraper import ScrapedResult
    
    # Valid result
    valid_result = ScrapedResult(
        draw_date=date(2026, 1, 15),
        winning_numbers=[1, 2, 3, 4, 5, 6],
        raw_data={}
    )
    assert scraper.validate(valid_result) is True
    
    # Invalid: future date
    future_result = ScrapedResult(
        draw_date=date(2027, 1, 1),
        winning_numbers=[1, 2, 3, 4, 5, 6],
        raw_data={}
    )
    assert scraper.validate(future_result) is False
    
    # Invalid: duplicate numbers
    duplicate_result = ScrapedResult(
        draw_date=date(2026, 1, 15),
        winning_numbers=[1, 1, 3, 4, 5, 6],
        raw_data={}
    )
    assert scraper.validate(duplicate_result) is False
    
    # Invalid: no numbers
    empty_result = ScrapedResult(
        draw_date=date(2026, 1, 15),
        winning_numbers=[],
        raw_data={}
    )
    assert scraper.validate(empty_result) is False


@pytest.mark.asyncio
async def test_sikkim_scraper_initialization():
    """Test Sikkim scraper initializes correctly"""
    scraper = IndiaSikkimLotteryScraper()
    
    assert scraper.name == "Sikkim State Lottery"
    assert "sikkimlotteries.com" in scraper.url
