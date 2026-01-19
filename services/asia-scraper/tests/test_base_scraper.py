import pytest
from datetime import date
from src.scrapers.base.base_scraper import BaseScraper, ScrapedResult


class MockScraper(BaseScraper):
    """Mock scraper for testing base functionality"""
    
    def __init__(self):
        super().__init__({
            'name': 'Mock Lottery',
            'url': 'https://example.com',
            'schedule': '0 0 * * *'
        })
    
    async def scrape(self):
        return [
            ScrapedResult(
                draw_date=date(2026, 1, 15),
                winning_numbers=[1, 2, 3, 4, 5, 6],
                raw_data={}
            )
        ]


@pytest.mark.asyncio
async def test_base_scraper_execute():
    """Test base scraper execute method"""
    scraper = MockScraper()
    results = await scraper.execute()
    
    assert len(results) == 1
    assert results[0].winning_numbers == [1, 2, 3, 4, 5, 6]


def test_scraped_result_validation():
    """Test ScrapedResult Pydantic model validation"""
    # Valid result
    valid = ScrapedResult(
        draw_date=date(2026, 1, 15),
        winning_numbers=[1, 2, 3, 4, 5, 6],
        raw_data={}
    )
    assert valid.draw_date == date(2026, 1, 15)
    assert len(valid.winning_numbers) == 6
    
    # With optional fields
    complete = ScrapedResult(
        draw_date=date(2026, 1, 15),
        draw_number="1234",
        winning_numbers=[1, 2, 3, 4, 5, 6],
        bonus_numbers=[7, 8],
        jackpot={"amount": 1000000, "currency": "USD"},
        winners_count=5,
        raw_data={"source": "test"}
    )
    assert complete.draw_number == "1234"
    assert complete.jackpot['amount'] == 1000000
    assert complete.winners_count == 5


def test_scraped_result_requires_winning_numbers():
    """Test that ScrapedResult requires at least one winning number"""
    with pytest.raises(Exception):  # Pydantic validation error
        ScrapedResult(
            draw_date=date(2026, 1, 15),
            winning_numbers=[],  # Empty list should fail min_length=1
            raw_data={}
        )


@pytest.mark.asyncio
async def test_base_scraper_validation():
    """Test base scraper validation method"""
    scraper = MockScraper()
    
    # Valid
    valid = ScrapedResult(
        draw_date=date(2026, 1, 15),
        winning_numbers=[1, 2, 3, 4, 5, 6],
        raw_data={}
    )
    assert scraper.validate(valid) is True
    
    # Future date (invalid)
    future = ScrapedResult(
        draw_date=date(2030, 1, 1),
        winning_numbers=[1, 2, 3, 4, 5, 6],
        raw_data={}
    )
    assert scraper.validate(future) is False
