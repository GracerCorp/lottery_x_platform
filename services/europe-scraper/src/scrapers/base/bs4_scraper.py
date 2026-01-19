"""BeautifulSoup4-based scraper for simple HTML parsing"""

import httpx
from bs4 import BeautifulSoup
from typing import Dict, List
from src.scrapers.base.base_scraper import BaseScraper


class BS4Scraper(BaseScraper):
    """Base scraper using BeautifulSoup4 for HTML parsing"""

    def __init__(self, slug: str):
        super().__init__(slug)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def fetch_html(self) -> str:
        """
        Fetch HTML content from URL
        
        Returns:
            HTML content as string
        """
        try:
            async with httpx.AsyncClient(headers=self.headers, timeout=30.0) as client:
                response = client.get(self.url)
                response.raise_for_status()
                return response.text
        except Exception as e:
            self.logger.error("Failed to fetch HTML", error=str(e))
            raise

    def parse_html(self, html: str) -> BeautifulSoup:
        """
        Parse HTML content with BeautifulSoup
        
        Args:
            html: HTML content
        
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, "lxml")

    def scrape(self) -> BeautifulSoup:
        """
        Scrape the lottery website
        
        Returns:
            BeautifulSoup object
        """
        self.logger.info("Fetching HTML", url=self.url)
        html = self.fetch_html()
        return self.parse_html(html)

    def parse_results(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parse results from BeautifulSoup object
        Override this method in subclasses
        
        Args:
            soup: BeautifulSoup object
        
        Returns:
            List of result dictionaries
        """
        raise NotImplementedError("Subclasses must implement parse_results method")
