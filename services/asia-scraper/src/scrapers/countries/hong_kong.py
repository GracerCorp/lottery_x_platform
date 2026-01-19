from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver
from src.scrapers.base.selenium_scraper import SeleniumScraper
from src.scrapers.base.base_scraper import ScrapedResult


class HongKongMarkSixScraper(SeleniumScraper):
    """Hong Kong Mark Six lottery scraper"""
    
    def __init__(self):
        super().__init__({
            "name": "Mark Six",
            "url": "https://bet.hkjc.com/marksix/",
            "schedule": "0 21 * * 2,4,6",  # Tue, Thu, Sat 9 PM HKT
        })
    
    async def parse_dynamic_content(
        self,
        soup: BeautifulSoup,
        driver: webdriver.Chrome
    ) -> List[ScrapedResult]:
        """Parse Mark Six results"""
        results = []

        try:
            # HKJC Mark Six draws 6 numbers + 1 extra number
            result_section = soup.find('div', class_='marksix_search_result')

            if result_section:
                # Main 6 numbers
                main_numbers = result_section.find_all('div', class_='ball_holder')[:6]
                winning_numbers = [
                    int(ball.find('div', class_='ball').text.strip())
                    for ball in main_numbers
                    if ball.find('div', class_='ball')
                ]
                
                # Extra number (bonus)
                extra_ball = result_section.find('div', class_='extra_ball')
                bonus_numbers = None
                if extra_ball:
                    extra_text = extra_ball.find('div', class_='ball')
                    if extra_text and extra_text.text.strip().isdigit():
                        bonus_numbers = [int(extra_text.text.strip())]
                
                # Get draw number
                draw_no = soup.find('div', class_='draw_no')
                draw_number = draw_no.text.strip() if draw_no else None
                
                # Get date
                draw_date_elem = soup.find('div', class_='date')
                from datetime import date, datetime
                draw_date = date.today()
                
                if draw_date_elem:
                    try:
                        date_text = draw_date_elem.text.strip()
                        draw_date = datetime.strptime(date_text, '%d/%m/%Y').date()
                    except:
                        pass
                
                if winning_numbers:
                    result = ScrapedResult(
                        draw_date=draw_date,
                        draw_number=draw_number,
                        winning_numbers=winning_numbers,
                        bonus_numbers=bonus_numbers,
                        raw_data={"source": "hkjc"}
                    )
                    results.append(result)
            
        except Exception as e:
            self.logger.error("Error parsing Mark Six", error=str(e))
        
        return results
