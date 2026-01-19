"""Mexican lottery scrapers"""

from typing import List, Dict
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.scrapers.base.selenium_scraper import SeleniumScraper
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MelateScraper(SeleniumScraper):
    """Scraper for Mexican Melate lottery"""
    
    def parse_results(self, driver) -> List[Dict]:
        """
        Parse Melate results from Pronósticos website
        
        Format expected:
        - 6 main numbers (1-56)
        - 1 additional number
        - Draw date
        """
        results = []
        
        try:
            # Wait for results to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "resultados"))
            )
            
            # Find Melate results
            melate_section = driver.find_element(By.ID, "melate-results")
            draw_items = melate_section.find_elements(By.CLASS_NAME, "sorteo")[:5]
            
            for item in draw_items:
                try:
                    # Extract date
                    date_elem = item.find_element(By.CLASS_NAME, "fecha")
                    draw_date = self._parse_spanish_date(date_elem.text)
                    
                    # Extract numbers
                    numbers = []
                    balls = item.find_elements(By.CLASS_NAME, "numero")
                    for ball in balls:
                        numbers.append(int(ball.text))
                    
                    # First 6 are main, 7th is additional
                    main_numbers = numbers[:6] if len(numbers) >= 6 else numbers
                    additional = numbers[6:7] if len(numbers) > 6 else []
                    
                    result = {
                        "draw_date": draw_date,
                        "numbers": {
                            "main": sorted(main_numbers)
                        },
                        "currency": "MXN"
                    }
                    
                    if additional:
                        result["numbers"]["bonus"] = additional
                    
                    results.append(result)
                    
                except Exception as e:
                    logger.error("Failed to parse Melate result", error=str(e))
                    continue
            
            logger.info("Parsed Melate results", count=len(results))
            return results
            
        except Exception as e:
            logger.error("Failed to parse Melate results", error=str(e))
            return []
    
    def _parse_spanish_date(self, date_text: str) -> datetime:
        """Parse Spanish date formats"""
        # Map Spanish month names to numbers
        spanish_months = {
            "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
            "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
            "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
        }
        
        try:
            # Replace Spanish month names with numbers
            date_lower = date_text.lower()
            for sp_month, num in spanish_months.items():
                if sp_month in date_lower:
                    date_lower = date_lower.replace(sp_month, num)
                    break
            
            # Try to parse
            formats = ["%d %m %Y", "%d-%m-%Y", "%Y-%m-%d"]
            for fmt in formats:
                try:
                    return datetime.strptime(date_lower.strip(), fmt)
                except ValueError:
                    continue
        except Exception as e:
            logger.error("Failed to parse Spanish date", date_text=date_text, error=str(e))
        
        logger.warning("Could not parse date, using current date", date_text=date_text)
        return datetime.now()


class ChispazoScraper(SeleniumScraper):
    """Scraper for Mexican Chispazo lottery"""
    
    def parse_results(self, driver) -> List[Dict]:
        """
        Parse Chispazo results (daily lottery)
        
        Format expected:
        - 5 numbers
        - Draw date and time
        """
        results = []
        
        try:
            # Wait for results
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "chispazo-results"))
            )
            
            # Find draws
            draws = driver.find_elements(By.CLASS_NAME, "chispazo-draw")[:10]
            
            for draw in draws:
                try:
                    # Extract date
                    date_elem = draw.find_element(By.CLASS_NAME, "fecha-hora")
                    draw_date = self._parse_spanish_date(date_elem.text)
                    
                    # Extract numbers
                    numbers = []
                    balls = draw.find_elements(By.CLASS_NAME, "bola")
                    for ball in balls:
                        numbers.append(int(ball.text))
                    
                    results.append({
                        "draw_date": draw_date,
                        "numbers": {
                            "main": sorted(numbers)
                        },
                        "currency": "MXN"
                    })
                    
                except Exception as e:
                    logger.error("Failed to parse Chispazo result", error=str(e))
                    continue
            
            logger.info("Parsed Chispazo results", count=len(results))
            return results
            
        except Exception as e:
            logger.error("Failed to parse Chispazo results", error=str(e))
            return []
    
    def _parse_spanish_date(self, date_text: str) -> datetime:
        """Parse Spanish date/time formats"""
        spanish_months = {
            "enero": "01", "febrero": "02", "marzo": "03", "abril": "04",
            "mayo": "05", "junio": "06", "julio": "07", "agosto": "08",
            "septiembre": "09", "octubre": "10", "noviembre": "11", "diciembre": "12"
        }
        
        try:
            date_lower = date_text.lower()
            for sp_month, num in spanish_months.items():
                if sp_month in date_lower:
                    date_lower = date_lower.replace(sp_month, num)
                    break
            
            formats = [
                "%d %m %Y %H:%M",
                "%d-%m-%Y %H:%M",
                "%Y-%m-%d %H:%M",
                "%d %m %Y",
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(date_lower.strip(), fmt)
                except ValueError:
                    continue
        except Exception as e:
            logger.error("Failed to parse Spanish date", date_text=date_text, error=str(e))
        
        logger.warning("Could not parse date, using current date", date_text=date_text)
        return datetime.now()
