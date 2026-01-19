from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from src.scrapers.base.selenium_scraper import SeleniumScraper
from src.scrapers.base.base_scraper import ScrapedResult


class PhilippinesPCSOLottoScraper(SeleniumScraper):
    """Philippines PCSO Lotto scraper"""
    
    def __init__(self):
        super().__init__({
            "name": "PCSO Lotto",
            "url": "https://www.pcso.gov.ph/SearchLottoResult.aspx",
            "schedule": "0 21 * * *",  # 9 PM daily
        })
    
    async def parse_dynamic_content(
        self, 
        soup: BeautifulSoup, 
        driver: webdriver.Chrome
    ) -> List[ScrapedResult]:
        """Parse PCSO Lotto results"""
        results = []
        
        try:
            # PCSO has multiple lotto games: 6/42, 6/45, 6/49, 6/55, 6/58
            result_table = soup.find('table', id='GridView1')
            
            if result_table:
                rows = result_table.find_all('tr')[1:]  # Skip header
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        # Parse date
                        date_str = cols[0].text.strip()
                        from datetime import datetime
                        draw_date = datetime.strptime(date_str, '%m/%d/%Y').date()
                        
                        # Parse game type (e.g., "Lotto 6/42")
                        game_type = cols[1].text.strip()
                        
                        # Parse winning numbers
                        numbers_str = cols[2].text.strip()
                        winning_numbers = [
                            int(n.strip()) 
                            for n in numbers_str.split('-') 
                            if n.strip().isdigit()
                        ]
                        
                        # Parse jackpot
                        jackpot = None
                        if len(cols) >= 4:
                            jackpot_str = cols[3].text.strip().replace(',', '')
                            if jackpot_str.replace('.', '').isdigit():
                                jackpot = {
                                    "amount": float(jackpot_str),
                                    "currency": "PHP"
                                }
                        
                        result = ScrapedResult(
                            draw_date=draw_date,
                            winning_numbers=winning_numbers,
                            jackpot=jackpot,
                            raw_data={"game_type": game_type}
                        )
                        results.append(result)
            
        except Exception as e:
            self.logger.error("Error parsing PCSO Lotto", error=str(e))
        
        return results
