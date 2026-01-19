"""Selenium-based scraper for JavaScript-heavy websites"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from typing import Dict, List
from src.scrapers.base.base_scraper import BaseScraper
from src.config.settings import settings


class SeleniumScraper(BaseScraper):
    """Base scraper using Selenium for JavaScript-heavy sites"""

    def __init__(self, slug: str):
        super().__init__(slug)
        self.driver = None

    def setup_driver(self) -> webdriver.Chrome:
        """
        Setup Chrome WebDriver with options
        
        Returns:
            Chrome WebDriver instance
        """
        chrome_options = Options()
        
        if settings.SELENIUM_HEADLESS:
            chrome_options.add_argument("--headless=new")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Disable images for faster loading
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(settings.SELENIUM_TIMEOUT)
        
        return driver

    def wait_for_element(self, by: By, value: str, timeout: int = None) -> any:
        """
        Wait for element to be present
        
        Args:
            by: By locator strategy
            value: Locator value
            timeout: Timeout in seconds (default: from settings)
        
        Returns:
            WebElement
        """
        if timeout is None:
            timeout = settings.SELENIUM_TIMEOUT
        
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def scrape(self) -> webdriver.Chrome:
        """
        Scrape the lottery website using Selenium
        
        Returns:
            WebDriver instance with loaded page
        """
        try:
            self.driver = self.setup_driver()
            self.logger.info("Loading page", url=self.url)
            self.driver.get(self.url)
            
            # Give page time to load JavaScript content
            self.driver.implicitly_wait(5)
            
            return self.driver
            
        except Exception as e:
            self.logger.error("Failed to load page", error=str(e))
            if self.driver:
                self.driver.quit()
            raise

    def parse_results(self, driver: webdriver.Chrome) -> List[Dict]:
        """
        Parse results from Selenium WebDriver
        Override this method in subclasses
        
        Args:
            driver: Selenium WebDriver
        
        Returns:
            List of result dictionaries
        """
        raise NotImplementedError("Subclasses must implement parse_results method")

    def cleanup(self) -> None:
        """Clean up Selenium driver"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.debug("Selenium driver closed")
            except Exception as e:
                self.logger.warning("Error closing driver", error=str(e))

    def run(self) -> Dict:
        """
        Run scraper with automatic cleanup
        
        Returns:
            Dict with execution summary
        """
        try:
            return super().run()
        finally:
            self.cleanup()
