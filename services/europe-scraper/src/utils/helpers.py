"""Helper utilities for data parsing and manipulation"""

import re
from datetime import datetime
from typing import List, Optional


def parse_european_date(date_str: str, formats: List[str] = None) -> Optional[datetime]:
    """
    Parse European date formats
    
    Args:
        date_str: Date string to parse
        formats: List of date formats to try (default: common European formats)
    
    Returns:
        datetime object or None
    """
    if formats is None:
        formats = [
            "%d/%m/%Y",  # 25/12/2024
            "%d-%m-%Y",  # 25-12-2024
            "%d.%m.%Y",  # 25.12.2024
            "%Y-%m-%d",  # 2024-12-25
            "%d %B %Y",  # 25 December 2024
            "%d %b %Y",  # 25 Dec 2024
        ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    
    return None


def parse_european_number(number_str: str) -> Optional[float]:
    """
    Parse European number formats (1.234.567,89 or 1 234 567,89)
    
    Args:
        number_str: Number string to parse
    
    Returns:
        float or None
    """
    try:
        # Remove spaces and convert European format to standard
        cleaned = number_str.replace(" ", "").replace(".", "").replace(",", ".")
        return float(cleaned)
    except (ValueError, AttributeError):
        return None


def extract_numbers(text: str) -> List[int]:
    """
    Extract all numbers from text
    
    Args:
        text: Text containing numbers
    
    Returns:
        List of integers
    """
    numbers = re.findall(r'\b\d+\b', text)
    return [int(n) for n in numbers]


def parse_currency(amount_str: str) -> tuple[Optional[float], Optional[str]]:
    """
    Parse currency amount and symbol
    
    Args:
        amount_str: Currency string like "€100M", "£50,000", "$1.5M"
    
    Returns:
        Tuple of (amount, currency_code)
    """
    currency_symbols = {
        "€": "EUR",
        "£": "GBP",
        "$": "USD",
        "CHF": "CHF",
        "kr": "SEK",
        "zł": "PLN",
    }
    
    # Extract currency symbol
    currency = None
    for symbol, code in currency_symbols.items():
        if symbol in amount_str:
            currency = code
            amount_str = amount_str.replace(symbol, "")
            break
    
    # Handle million/billion suffixes
    multiplier = 1
    if "M" in amount_str.upper():
        multiplier = 1_000_000
        amount_str = amount_str.upper().replace("M", "")
    elif "B" in amount_str.upper():
        multiplier = 1_000_000_000
        amount_str = amount_str.upper().replace("B", "")
    
    # Parse the number
    amount = parse_european_number(amount_str)
    if amount:
        amount *= multiplier
    
    return amount, currency


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Text to clean
    
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text
