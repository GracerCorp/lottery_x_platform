"""Data validators for lottery results"""

from datetime import datetime
from typing import Dict, List


def validate_result_data(result: Dict) -> bool:
    """
    Validate lottery result data structure
    
    Args:
        result: Result dictionary to validate
    
    Returns:
        True if valid, False otherwise
    """
    # Required fields
    if "draw_date" not in result:
        return False
    
    if not isinstance(result["draw_date"], datetime):
        return False
    
    if "numbers" not in result:
        return False
    
    numbers = result["numbers"]
    if not isinstance(numbers, dict):
        return False
    
    # Must have main numbers
    if "main" not in numbers:
        return False
    
    if not isinstance(numbers["main"], list):
        return False
    
    if len(numbers["main"]) == 0:
        return False
    
    # All numbers must be integers
    for num in numbers["main"]:
        if not isinstance(num, int):
            return False
    
    # Bonus numbers if present
    if "bonus" in numbers:
        if not isinstance(numbers["bonus"], list):
            return False
        for num in numbers["bonus"]:
            if not isinstance(num, int):
                return False
    
    # Currency if present
    if "currency" in result:
        if not isinstance(result["currency"], str):
            return False
    
    return True


def validate_currency(currency: str) -> bool:
    """Validate currency code"""
    valid_currencies = ["USD", "CAD", "MXN", "CRC", "PAB", "GTQ", "HNL", "NIO", "JMD", "DOP", "HTG", "BBD", "XCD"]
    return currency in valid_currencies


def validate_number_range(numbers: List[int], min_val: int, max_val: int) -> bool:
    """Validate numbers are within expected range"""
    for num in numbers:
        if not (min_val <= num <= max_val):
            return False
    return True
