"""
Test runner script for the Asia lottery scraper

Usage:
    poetry run python run_tests.py          # Run all tests
    poetry run python run_tests.py -v       # Verbose output
    poetry run python run_tests.py -k india # Run only India tests
"""

import sys
import pytest


def main():
    """Run pytest with custom arguments"""
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # Default args if none provided
    if not args:
        args = ['-v', 'tests/']
    
    exit_code = pytest.main(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
