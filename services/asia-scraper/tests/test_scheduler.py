import pytest
from src.services.scheduler import parse_cron_expression


def test_parse_cron_simple():
    """Test parsing simple cron expressions"""
    # Daily at midnight
    result = parse_cron_expression("0 0 * * *")
    assert result == {'minute': '0', 'hour': '0'}
    
    # Every hour
    result = parse_cron_expression("0 * * * *")
    assert result == {'minute': '0'}
    
    # Specific time
    result = parse_cron_expression("30 14 * * *")
    assert result == {'minute': '30', 'hour': '14'}


def test_parse_cron_with_days():
    """Test parsing cron with specific days"""
    # Mon, Wed, Fri
    result = parse_cron_expression("0 9 * * 1,3,5")
    assert result['minute'] == '0'
    assert result['hour'] == '9'
    assert result['day_of_week'] == '1,3,5'


def test_parse_cron_with_dates():
    """Test parsing cron with specific dates"""
    # 1st and 15th of month
    result = parse_cron_expression("0 12 1,15 * *")
    assert result['minute'] == '0'
    assert result['hour'] == '12'
    assert result['day'] == '1,15'


def test_parse_cron_invalid():
    """Test that invalid cron expressions raise errors"""
    with pytest.raises(ValueError):
        parse_cron_expression("invalid")
    
    with pytest.raises(ValueError):
        parse_cron_expression("0 0 *")  # Too few parts
    
    with pytest.raises(ValueError):
        parse_cron_expression("0 0 * * * *")  # Too many parts
