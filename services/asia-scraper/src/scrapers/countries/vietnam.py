from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from src.scrapers.base.selenium_scraper import SeleniumScraper
from src.scrapers.base.base_scraper import ScrapedResult


class VietnamVietlottScraper(SeleniumScraper):
    """Vietnam Vietlott scraper"""
    
    def __init__(self):
        super().__init__({
            "name": "Vietlott",
            "url": "https://vietlott.vn/",
            "schedule": "0 18 * * 2,4,6",  # Tue, Thu, Sat 6 PM ICT
        })
    
    async def parse_dynamic_content(
        self, 
        soup: BeautifulSoup, 
        driver: webdriver.Chrome
    ) -> List[ScrapedResult]:
        """Parse Vietlott results"""
        results = []
        
        try:
            # Vietlott has multiple games: Mega 6/45, Power 6/55, Max 3D, Max 4D
            result_container = soup.find('div', class_='result-container')
            
            if result_container:
                # Find numbers (typically in spans or divs with class 'number' or 'ball')
                number_elements = result_container.find_all(['span', 'div'], class_=['number', 'ball'])
                winning_numbers = []
                
                for elem in number_elements:
                    text = elem.text.strip()
                    if text.isdigit():
                        winning_numbers.append(int(text))
                
                # Get game type
                game_type_elem = soup.find('div', class_='game-name')
                game_type = game_type_elem.text.strip() if game_type_elem else None
                
                # Get draw date
                date_elem = soup.find('span', class_='draw-date')
                from datetime import date, datetime
                draw_date = date.today()
                
                if date_elem:
                    try:
                        date_text = date_elem.text.strip()
                        # Vietnamese date format: dd/mm/yyyy
                        draw_date = datetime.strptime(date_text, '%d/%m/%Y').date()
                    except:
                        pass
                
                if winning_numbers:
                    result = ScrapedResult(
                        draw_date=draw_date,
                        winning_numbers=winning_numbers,
                        raw_data={
                            "game_type": game_type,
                            "country": "vietnam"
                        }
                    )
                    results.append(result)
            
        except Exception as e:
            self.logger.error("Error parsing Vietlott", error=str(e))
        
        return results
