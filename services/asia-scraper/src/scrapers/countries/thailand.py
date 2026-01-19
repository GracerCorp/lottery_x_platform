from typing import List
from bs4 import BeautifulSoup
from src.scrapers.base.bs4_scraper import BS4Scraper
from src.scrapers.base.base_scraper import ScrapedResult


class ThailandGovernmentLotteryScraper(BS4Scraper):
    """Thailand Government Lottery scraper"""
    
    def __init__(self):
        super().__init__({
            "name": "Thailand Government Lottery",
            "url": "https://news.sanook.com/lotto/",
            "schedule": "0 15 1,16 * *",  # 1st and 16th of month at 3 PM
        })
    
    async def parse_html(self, soup: BeautifulSoup) -> List[ScrapedResult]:
        """Parse Thailand lottery results"""
        results = []
        
        try:
            # Thai lottery has 6-digit winning numbers
            prize_div = soup.find('div', class_='lotto-check__result')
            
            if prize_div:
                # First prize (6 digits)
                first_prize = prize_div.find('strong', class_='lotto-check__number')
                if first_prize:
                    number_str = first_prize.text.strip()
                    winning_numbers = [int(d) for d in number_str if d.isdigit()]
                    
                    # Get draw date
                    date_elem = soup.find('span', class_='lotto-check__date')
                    if date_elem:
                        # Parse Thai date format
                        # Example: "1 มกราคม 2569" -> need to convert from Thai calendar
                        # Simplified: use current date for now
                        from datetime import date
                        draw_date = date.today()
                        
                        result = ScrapedResult(
                            draw_date=draw_date,
                            winning_numbers=winning_numbers,
                            raw_data={"lottery_type": "government"}
                        )
                        results.append(result)
            
        except Exception as e:
            self.logger.error("Error parsing Thailand lottery", error=str(e))
        
        return results
