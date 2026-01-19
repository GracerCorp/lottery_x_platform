"""Basic test suite for Europe lottery scraper"""

import pytest
from src.utils.helpers import (
    parse_european_date,
    parse_european_number,
    parse_currency,
    extract_numbers
)


class TestHelpers:
    """Test helper utilities"""
    
    def test_parse_european_date(self):
        """Test European date parsing"""
        # DD/MM/YYYY format
        date1 = parse_european_date("25/12/2024")
        assert date1 is not None
        assert date1.day == 25
        assert date1.month == 12
        assert date1.year == 2024
        
        # DD-MM-YYYY format
        date2 = parse_european_date("31-01-2024")
        assert date2 is not None
        assert date2.day == 31
        assert date2.month == 1
        
    def test_parse_european_number(self):
        """Test European number format parsing"""
        # European format with comma decimal
        num1 = parse_european_number("1.234.567,89")
        assert num1 == 1234567.89
        
        # Space-separated thousands
        num2 = parse_european_number("1 234 567,89")
        assert num2 == 1234567.89
        
    def test_parse_currency(self):
        """Test currency parsing"""
        # Euros with million suffix
        amount1, currency1 = parse_currency("€100M")
        assert amount1 == 100_000_000
        assert currency1 == "EUR"
        
        # British pounds
        amount2, currency2 = parse_currency("£50,000")
        assert amount2 == 50000
        assert currency2 == "GBP"
        
    def test_extract_numbers(self):
        """Test number extraction from text"""
        numbers = extract_numbers("The winning numbers are 7, 14, 21, 28, 35, 42")
        assert numbers == [7, 14, 21, 28, 35, 42]


class TestConfig:
    """Test configuration loading"""
    
    def test_lottery_config_loading(self):
        """Test that lottery configurations load correctly"""
        from src.config.countries import ALL_COUNTRIES, get_lottery_config
        
        assert len(ALL_COUNTRIES) > 0
        
        # Test getting a specific lottery
        uk_lottery = get_lottery_config("uk-national-lottery")
        assert uk_lottery is not None
        assert uk_lottery["name"] == "UK National Lottery"
        assert uk_lottery["country_code"] == "GB"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
