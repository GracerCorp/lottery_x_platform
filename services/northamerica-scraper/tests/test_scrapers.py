"""Unit tests for scraper parsing logic"""

import pytest
from datetime import datetime
from src.utils.validators import validate_result_data, validate_currency, validate_number_range


class TestValidators:
    """Test data validators"""
    
    def test_validate_result_data_valid(self):
        """Test valid result data"""
        result = {
            "draw_date": datetime(2024, 1, 15),
            "numbers": {
                "main": [1, 2, 3, 4, 5],
                "bonus": [6]
            },
            "jackpot": "$100M",
            "currency": "USD"
        }
        assert validate_result_data(result) is True
    
    def test_validate_result_data_missing_date(self):
        """Test missing draw date"""
        result = {
            "numbers": {
                "main": [1, 2, 3, 4, 5]
            }
        }
        assert validate_result_data(result) is False
    
    def test_validate_result_data_missing_numbers(self):
        """Test missing numbers"""
        result = {
            "draw_date": datetime(2024, 1, 15)
        }
        assert validate_result_data(result) is False
    
    def test_validate_currency(self):
        """Test currency validation"""
        assert validate_currency("USD") is True
        assert validate_currency("CAD") is True
        assert validate_currency("MXN") is True
        assert validate_currency("INVALID") is False
    
    def test_validate_number_range(self):
        """Test number range validation"""
        # Powerball main numbers (1-69)
        assert validate_number_range([1, 10, 20, 30, 40], 1, 69) is True
        assert validate_number_range([1, 10, 20, 30, 70], 1, 69) is False
        assert validate_number_range([0, 10, 20, 30, 40], 1, 69) is False


@pytest.mark.unit
class TestScraperConfig:
    """Test scraper configuration"""
    
    def test_lottery_slugs(self):
        """Test all lottery slugs are unique"""
        from src.config.countries import get_all_lottery_slugs
        
        slugs = get_all_lottery_slugs()
        assert len(slugs) == len(set(slugs)), "Duplicate lottery slugs found"
    
    def test_get_lottery_config(self):
        """Test getting lottery config by slug"""
        from src.config.countries import get_lottery_config
        
        # Test existing lottery
        config = get_lottery_config("us-powerball")
        assert config is not None
        assert config["name"] == "Powerball"
        assert config["country_name"] == "United States"
        
        # Test non-existing lottery
        config = get_lottery_config("invalid-slug")
        assert config is None
    
    def test_cron_schedules(self):
        """Test all lotteries have valid CRON schedules"""
        from src.config.countries import ALL_COUNTRIES
        
        for country in ALL_COUNTRIES:
            for lottery in country.lotteries:
                assert "schedule" in lottery
                # Basic CRON validation (5 parts)
                parts = lottery["schedule"].split()
                assert len(parts) == 5, f"Invalid CRON for {lottery['slug']}"
