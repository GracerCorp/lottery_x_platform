"""Canadian lottery scrapers"""

from typing import List, Dict
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.scrapers.base.selenium_scraper import SeleniumScraper
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Lotto649Scraper(SeleniumScraper):
    """Scraper for Canadian Lotto 6/49"""
    
    def parse_results(self, driver) -> List[Dict]:
        """
        Parse Lotto 6/49 results from OLG website
        
        Format expected:
        - 6 main numbers (1-49)
        - 1 bonus number (1-49)
        - Draw date
        """
        results = []
        
        try:
            # Wait for results section
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lotto-results"))
            )
            
            # Find recent draws
            draw_containers = driver.find_elements(By.CLASS_NAME, "draw-container")[:5]
            
            for container in draw_containers:
                try:
                    # Extract date
                    date_elem = container.find_element(By.CLASS_NAME, "draw-date")
                    draw_date = self._parse_date(date_elem.text)
                    
                    # Extract main numbers
                    main_numbers = []
                    number_elements = container.find_elements(By.CLASS_NAME, "ball-number")
                    for i, num_elem in enumerate(number_elements):
                        num = int(num_elem.text)
                        if i < 6:  # First 6 are main numbers
                            main_numbers.append(num)
                        else:  # 7th is bonus
                            bonus_number = num
                    
                    results.append({
                        "draw_date": draw_date,
                        "numbers": {
                            "main": sorted(main_numbers),
                            "bonus": [bonus_number]
                        },
                        "currency": "CAD"
                    })
                    
                except Exception as e:
                    logger.error("Failed to parse Lotto 6/49 result", error=str(e))
                    continue
            
            logger.info("Parsed Lotto 6/49 results", count=len(results))
            return results
            
        except Exception as e:
            logger.error("Failed to parse Lotto 6/49 results", error=str(e))
            return []
    
    def _parse_date(self, date_text: str) -> datetime:
        """Parse Canadian date formats"""
        formats = [
            "%b %d, %Y",
            "%B %d, %Y",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_text.strip(), fmt)
            except ValueError:
                continue
        
        logger.warning("Could not parse date, using current date", date_text=date_text)
        return datetime.now()


class LottoMaxScraper(SeleniumScraper):
    """Scraper for Canadian Lotto Max"""
    
    def parse_results(self, driver) -> List[Dict]:
        """
        Parse Lotto Max results from OLG website
        
        Format expected:
        - 7 main numbers (1-50)
        - Draw date
        - Jackpot amount
        """
        results = []
        
        try:
            # Wait for results
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "max-results"))
            )
            
            # Find recent draws
            draws = driver.find_elements(By.CLASS_NAME, "max-draw")[:5]
            
            for draw in draws:
                try:
                    # Extract date
                    date_text = draw.find_element(By.CLASS_NAME, "date").text
                    draw_date = self._parse_date(date_text)
                    
                    # Extract numbers (7 main numbers)
                    main_numbers = []
                    balls = draw.find_elements(By.CLASS_NAME, "number-ball")
                    for ball in balls[:7]:
                        main_numbers.append(int(ball.text))
                    
                    # Extract jackpot if available
                    jackpot = None
                    try:
                        jackpot_elem = draw.find_element(By.CLASS_NAME, "jackpot")
                        jackpot = jackpot_elem.text.strip()
                    except:
                        pass
                    
                    result = {
                        "draw_date": draw_date,
                        "numbers": {
                            "main": sorted(main_numbers)
                        },
                        "currency": "CAD"
                    }
                    
                    if jackpot:
                        result["jackpot"] = jackpot
                    
                    results.append(result)
                    
                except Exception as e:
                    logger.error("Failed to parse Lotto Max result", error=str(e))
                    continue
            
            logger.info("Parsed Lotto Max results", count=len(results))
            return results
            
        except Exception as e:
            logger.error("Failed to parse Lotto Max results", error=str(e))
            return []
    
    def _parse_date(self, date_text: str) -> datetime:
        """Parse Canadian date formats"""
        formats = [
            "%b %d, %Y",
            "%B %d, %Y",
            "%Y-%m-%d",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_text.strip(), fmt)
            except ValueError:
                continue
        
        logger.warning("Could not parse date, using current date", date_text=date_text)
        return datetime.now()
