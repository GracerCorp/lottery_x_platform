import httpx
from bs4 import BeautifulSoup
from typing import List
from src.scrapers.base.base_scraper import BaseScraper, ScrapedResult
from src.config.settings import settings


class BS4Scraper(BaseScraper):
    """Scraper for static HTML using BeautifulSoup"""
    
    async def fetch_html(self, url: str) -> BeautifulSoup:
        """Fetch and parse HTML"""
        async with httpx.AsyncClient(timeout=settings.DEFAULT_TIMEOUT) as client:
            headers = {"User-Agent": settings.SCRAPER_USER_AGENT}
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            
            self.logger.debug("Fetched HTML", url=url, status=response.status_code)
            return BeautifulSoup(response.text, 'lxml')
    
    async def scrape(self) -> List[ScrapedResult]:
        """Default scrape implementation"""
        soup = await self.fetch_html(self.url)
        return await self.parse_html(soup)
    
    async def parse_html(self, soup: BeautifulSoup) -> List[ScrapedResult]:
        """Parse HTML - must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement parse_html")
