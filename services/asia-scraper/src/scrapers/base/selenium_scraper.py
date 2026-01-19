from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from typing import List
from src.scrapers.base.base_scraper import BaseScraper, ScrapedResult
from src.config.settings import settings


class SeleniumScraper(BaseScraper):
    """Scraper for dynamic JavaScript-rendered sites using Selenium"""
    
    def get_driver(self) -> webdriver.Chrome:
        """Create and configure Chrome driver"""
        chrome_options = Options()
        
        if settings.HEADLESS_MODE:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f'user-agent={settings.SCRAPER_USER_AGENT}')
        
        service = Service(executable_path=settings.CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(settings.DEFAULT_TIMEOUT)
        
        return driver
    
    async def scrape(self) -> List[ScrapedResult]:
        """Default scrape implementation using Selenium"""
        driver = None
        try:
            driver = self.get_driver()
            self.logger.debug("Selenium driver created", url=self.url)
            
            driver.get(self.url)
            self.logger.debug("Page loaded", title=driver.title)
            
            # Wait for dynamic content
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            
            # Get page source and parse
            soup = BeautifulSoup(driver.page_source, 'lxml')
            return await self.parse_dynamic_content(soup, driver)
            
        finally:
            if driver:
                driver.quit()
                self.logger.debug("Selenium driver closed")
    
    async def parse_dynamic_content(
        self, 
        soup: BeautifulSoup, 
        driver: webdriver.Chrome
    ) -> List[ScrapedResult]:
        """Parse dynamic content - must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement parse_dynamic_content")
