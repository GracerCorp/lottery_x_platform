"""United States lottery scrapers"""

from typing import List, Dict
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.scrapers.base.selenium_scraper import SeleniumScraper
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PowerballScraper(SeleniumScraper):
    """Scraper for US Powerball lottery"""
    
    def parse_results(self, driver) -> List[Dict]:
        """
        Parse Powerball results from the page
        
        Format expected:
        - 5 main numbers (1-69)
        - 1 Powerball number (1-26)
        - Draw date
        - Jackpot amount
        """
        results = []
        
        try:
            # Wait for results to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "game-result"))
            )
            
            # Find all result containers (get last 5 draws)
            result_elements = driver.find_elements(By.CLASS_NAME, "game-result")[:5]
            
            for element in result_elements:
                try:
                    # Extract date
                    date_text = element.find_element(By.CLASS_NAME, "draw-date").text
                    draw_date = self._parse_date(date_text)
                    
                    # Extract main numbers
                    main_numbers = []
                    number_elements = element.find_elements(By.CLASS_NAME, "white-ball")
                    for num_elem in number_elements:
                        main_numbers.append(int(num_elem.text))
                    
                    # Extract Powerball
                    powerball_elem = element.find_element(By.CLASS_NAME, "red-ball")
                    powerball = int(powerball_elem.text)
                    
                    # Extract jackpot
                    jackpot = "Unknown"
                    try:
                        jackpot_elem = element.find_element(By.CLASS_NAME, "jackpot-amount")
                        jackpot = jackpot_elem.text.strip()
                    except:
                        pass
                    
                    results.append({
                        "draw_date": draw_date,
                        "numbers": {
                            "main": sorted(main_numbers),
                            "bonus": [powerball]
                        },
                        "jackpot": jackpot,
                        "currency": "USD"
                    })
                    
                except Exception as e:
                    logger.error("Failed to parse Powerball result", error=str(e))
                    continue
            
            logger.info("Parsed Powerball results", count=len(results))
            return results
            
        except Exception as e:
            logger.error("Failed to parse Powerball results", error=str(e))
            return []
    
    def _parse_date(self, date_text: str) -> datetime:
        """Parse date from various formats"""
        # Try common formats
        formats = [
            "%m/%d/%Y",
            "%B %d, %Y",
            "%b %d, %Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_text.strip(), fmt)
            except ValueError:
                continue
        
        # Fallback to current date if parsing fails
        logger.warning("Could not parse date, using current date", date_text=date_text)
        return datetime.now()


class MegaMillionsScraper(SeleniumScraper):
    """Scraper for US Mega Millions lottery"""
    
    def parse_results(self, driver) -> List[Dict]:
        """
        Parse Mega Millions results from the page
        
        Format expected:
        - 5 main numbers (1-70)
        - 1 Mega Ball number (1-25)
        - Draw date
        - Jackpot amount
        """
        results = []
        
        try:
            # Wait for results to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "winning-numbers"))
            )
            
            # Find recent draws
            draw_elements = driver.find_elements(By.CLASS_NAME, "draw-item")[:5]
            
            for element in draw_elements:
                try:
                    # Extract date
                    date_elem = element.find_element(By.CLASS_NAME, "draw-date")
                    draw_date = self._parse_date(date_elem.text)
                    
                    # Extract numbers
                    main_numbers = []
                    white_balls = element.find_elements(By.CLASS_NAME, "number-white")
                    for ball in white_balls:
                        main_numbers.append(int(ball.text))
                    
                    # Extract Mega Ball
                    mega_ball = element.find_element(By.CLASS_NAME, "number-gold")
                    mega_ball_num = int(mega_ball.text)
                    
                    # Extract jackpot
                    jackpot = "Unknown"
                    try:
                        jackpot_elem = element.find_element(By.CLASS_NAME, "jackpot-text")
                        jackpot = jackpot_elem.text.strip()
                    except:
                        pass
                    
                    results.append({
                        "draw_date": draw_date,
                        "numbers": {
                            "main": sorted(main_numbers),
                            "bonus": [mega_ball_num]
                        },
                        "jackpot": jackpot,
                        "currency": "USD"
                    })
                    
                except Exception as e:
                    logger.error("Failed to parse Mega Millions result", error=str(e))
                    continue
            
            logger.info("Parsed Mega Millions results", count=len(results))
            return results
            
        except Exception as e:
            logger.error("Failed to parse Mega Millions results", error=str(e))
            return []
    
    def _parse_date(self, date_text: str) -> datetime:
        """Parse date from various formats"""
        formats = [
            "%m/%d/%Y",
            "%B %d, %Y",
            "%b %d, %Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_text.strip(), fmt)
            except ValueError:
                continue
        
        logger.warning("Could not parse date, using current date", date_text=date_text)
        return datetime.now()
