"""Example scraper for Spain lotteries"""

from typing import Dict, List
from bs4 import BeautifulSoup
from src.scrapers.base.bs4_scraper import BS4Scraper
from src.utils.helpers import parse_european_date, extract_numbers


class SpainPrimitivaScraper(BS4Scraper):
    """Scraper for La Primitiva (Spain)"""

    def parse_results(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse La Primitiva results"""
        results = []
        
        try:
            # Example parsing logic (adjust based on actual HTML)
            result_rows = soup.find_all("div", class_="resultado")
            
            for row in result_rows[:10]:  # Get last 10 draws
                try:
                    # Extract date
                    date_elem = row.find("span", class_="fecha")
                    if not date_elem:
                        continue
                    
                    draw_date = parse_european_date(date_elem.text)
                    if not draw_date:
                        continue
                    
                    # Extract numbers
                    numbers_elem = row.find("div", class_="bolas")
                    if numbers_elem:
                        number_texts = [ball.text for ball in numbers_elem.find_all("span", class_="bola")]
                        main_numbers = [int(n) for n in number_texts[:6]]
                        complement = [int(number_texts[6])] if len(number_texts) > 6 else []
                        reintegro = [int(number_texts[7])] if len(number_texts) > 7 else []
                    
                    results.append({
                        "draw_date": draw_date,
                        "numbers": {
                            "main": sorted(main_numbers),
                            "complement": complement,
                            "reintegro": reintegro
                        },
                        "currency": "EUR"
                    })
                    
                except Exception as e:
                    self.logger.warning("Failed to parse result row", error=str(e))
                    continue
            
        except Exception as e:
            self.logger.error("Failed to parse La Primitiva results", error=str(e))
            raise
        
        return results
