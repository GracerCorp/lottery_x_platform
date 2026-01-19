from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from datetime import date
from src.utils.logger import get_logger


class ScrapedResult(BaseModel):
    """Pydantic model for scraped lottery results"""
    draw_date: date
    draw_number: str | None = None
    winning_numbers: List[int] = Field(min_length=1)
    bonus_numbers: List[int] | None = None
    jackpot: Dict[str, Any] | None = None
    winners_count: int | None = None
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "draw_date": "2026-01-19",
                "draw_number": "1234",
                "winning_numbers": [1, 5, 12, 23, 34, 45],
                "bonus_numbers": [7],
                "jackpot": {"amount": 1000000, "currency": "SGD"},
                "winners_count": 3,
                "raw_data": {}
            }
        }


class BaseScraper(ABC):
    """Abstract base class for all scrapers"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.name = config.get("name", "Unknown")
        self.url = config.get("url", "")
    
    @abstractmethod
    async def scrape(self) -> List[ScrapedResult]:
        """Main scraping method - must be implemented by subclasses"""
        pass
    
    def validate(self, result: ScrapedResult) -> bool:
        """Validate a scraped result"""
        try:
            # Basic validation
            if not result.winning_numbers:
                self.logger.warning("No winning numbers found", result=result.dict())
                return False
            
            if result.draw_date > date.today():
                self.logger.warning("Draw date is in the future", date=result.draw_date)
                return False
            
            # Check for duplicate numbers
            if len(result.winning_numbers) != len(set(result.winning_numbers)):
                self.logger.warning("Duplicate winning numbers found", numbers=result.winning_numbers)
                return False
            
            return True
        except Exception as e:
            self.logger.error("Validation error", error=str(e))
            return False
    
    async def execute(self) -> List[ScrapedResult]:
        """Execute scraper with error handling"""
        self.logger.info("Starting scraper", scraper=self.name, url=self.url)
        
        try:
            results = await self.scrape()
            valid_results = [r for r in results if self.validate(r)]
            
            self.logger.info(
                "Scraper completed",
                scraper=self.name,
                total=len(results),
                valid=len(valid_results)
            )
            
            return valid_results
        except Exception as e:
            self.logger.error("Scraper failed", scraper=self.name, error=str(e), exc_info=True)
            raise
