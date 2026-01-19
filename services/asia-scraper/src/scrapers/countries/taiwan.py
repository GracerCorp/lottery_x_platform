from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from src.scrapers.base.selenium_scraper import SeleniumScraper
from src.scrapers.base.base_scraper import ScrapedResult


class TaiwanWelfareLotteryScraper(SeleniumScraper):
    """Taiwan Public Welfare Lottery scraper"""
    
    def __init__(self):
        super().__init__({
            "name": "Taiwan Public Welfare Lottery",
            "url": "https://www.pec.org.tw/",
            "schedule": "0 20 * * 1,4",  # Mon, Thu 8 PM CST
        })
    
    async def parse_dynamic_content(
        self, 
        soup: BeautifulSoup, 
        driver: webdriver.Chrome
    ) -> List[ScrapedResult]:
        """Parse Taiwan lottery results"""
        results = []
        
        try:
            # Taiwan lottery typically uses traditional Chinese characters
            # Look for results section
            result_box = soup.find('div', class_='lottery-result')
            
            if result_box:
                # Parse numbers
                number_spans = result_box.find_all('span', class_='ball')
                winning_numbers = [
                    int(span.text.strip())
                    for span in number_spans
                    if span.text.strip().isdigit()
                ]
                
                # Get draw date
                date_elem = soup.find('div', class_='draw-date')
                from datetime import date, datetime
                draw_date = date.today()
                
                if date_elem:
                    try:
                        date_text = date_elem.text.strip()
                        # Parse date (format may vary)
                        draw_date = datetime.strptime(date_text, '%Y-%m-%d').date()
                    except:
                        pass
                
                if winning_numbers:
                    result = ScrapedResult(
                        draw_date=draw_date,
                        winning_numbers=winning_numbers,
                        raw_data={"country": "taiwan"}
                    )
                    results.append(result)
            
        except Exception as e:
            self.logger.error("Error parsing Taiwan lottery", error=str(e))
        
        return results
