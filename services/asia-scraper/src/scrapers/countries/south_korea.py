from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from src.scrapers.base.selenium_scraper import SeleniumScraper
from src.scrapers.base.base_scraper import ScrapedResult


class SouthKoreaLotto645Scraper(SeleniumScraper):
    """South Korea Lotto 6/45 scraper"""
    
    def __init__(self):
        super().__init__({
            "name": "Lotto 6/45",
            "url": "https://www.dhlottery.co.kr/",
            "schedule": "0 20 * * 6",  # Saturday 8 PM KST
        })
    
    async def parse_dynamic_content(
        self, 
        soup: BeautifulSoup, 
        driver: webdriver.Chrome
    ) -> List[ScrapedResult]:
        """Parse Lotto 6/45 results"""
        results = []
        
        try:
            # Korean lottery site structure
            # Look for main winning numbers (6 numbers)
            number_divs = soup.find_all('div', class_='ball_645')
            
            if len(number_divs) >= 6:
                winning_numbers = [
                    int(div.text.strip()) 
                    for div in number_divs[:6]
                    if div.text.strip().isdigit()
                ]
                
                # Bonus number (7th number)
                bonus_number = None
                if len(number_divs) >= 7:
                    bonus_text = number_divs[6].text.strip()
                    if bonus_text.isdigit():
                        bonus_number = [int(bonus_text)]
                
                # Get draw number and date
                draw_info = soup.find('div', class_='win_result')
                draw_number = None
                if draw_info:
                    draw_text = draw_info.find('strong')
                    if draw_text:
                        draw_number = draw_text.text.strip()
                
                from datetime import date
                result = ScrapedResult(
                    draw_date=date.today(),
                    draw_number=draw_number,
                    winning_numbers=winning_numbers,
                    bonus_numbers=bonus_number,
                    raw_data={"lottery_type": "lotto645"}
                )
                results.append(result)
            
        except Exception as e:
            self.logger.error("Error parsing Lotto 6/45", error=str(e))
        
        return results
