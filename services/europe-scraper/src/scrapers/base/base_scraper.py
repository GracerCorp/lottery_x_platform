"""Base scraper class for all lottery scrapers"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from src.database.session import get_db
from src.database.models import Lottery, Result, ScraperJob
from src.utils.logger import get_logger
from src.config.countries import get_lottery_config

logger = get_logger(__name__)


class BaseScraper(ABC):
    """Abstract base class for lottery scrapers"""

    def __init__(self, slug: str):
        self.slug = slug
        self.config = get_lottery_config(slug)
        if not self.config:
            raise ValueError(f"No configuration found for lottery slug: {slug}")
        
        self.url = self.config["url"]
        self.name = self.config["name"]
        self.logger = logger.bind(slug=slug)

    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Scrape lottery results from the website
        
        Returns:
            List of result dictionaries
        """
        pass

    @abstractmethod
    def parse_results(self, raw_data: any) -> List[Dict]:
        """
        Parse raw scraped data into structured results
        
        Args:
            raw_data: Raw data from scraping
        
        Returns:
            List of parsed result dictionaries
        """
        pass

    def save_results(self, results: List[Dict], db: Session) -> int:
        """
        Save results to database with deduplication
        
        Args:
            results: List of result dictionaries
            db: Database session
        
        Returns:
            Number of new results saved
        """
        saved_count = 0
        
        # Get lottery ID
        lottery = db.query(Lottery).filter(Lottery.slug == self.slug).first()
        if not lottery:
            self.logger.error("Lottery not found in database", slug=self.slug)
            return 0
        
        for result in results:
            try:
                # Check if result already exists
                existing = db.query(Result).filter(
                    Result.lotteryId == lottery.id,
                    Result.drawDate == result["draw_date"]
                ).first()
                
                if existing:
                    self.logger.debug("Result already exists, skipping", 
                                     draw_date=result["draw_date"])
                    continue
                
                # Create new result
                new_result = Result(
                    lotteryId=lottery.id,
                    drawDate=result["draw_date"],
                    numbers=result["numbers"],
                    jackpot=result.get("jackpot"),
                    currency=result.get("currency", "EUR"),
                    winners=result.get("winners")
                )
                
                db.add(new_result)
                saved_count += 1
                
            except Exception as e:
                self.logger.error("Failed to save result", 
                                error=str(e), 
                                result=result)
        
        try:
            db.commit()
            self.logger.info("Saved results to database", count=saved_count)
        except Exception as e:
            db.rollback()
            self.logger.error("Failed to commit results", error=str(e))
            raise
        
        return saved_count

    def run(self) -> Dict:
        """
        Run the complete scraping process
        
        Returns:
            Dict with execution summary
        """
        start_time = datetime.now()
        db = get_db()
        
        # Get lottery for job tracking
        lottery = db.query(Lottery).filter(Lottery.slug == self.slug).first()
        job_id = None
        
        try:
            # Create job record
            if lottery:
                job = ScraperJob(
                    lotteryId=lottery.id,
                    status="running",
                    startedAt=start_time
                )
                db.add(job)
                db.commit()
                job_id = job.id
            
            self.logger.info("Starting scrape", job_id=job_id)
            
            # Scrape results
            raw_results = self.scrape()
            
            # Parse results
            parsed_results = self.parse_results(raw_results)
            
            # Save to database
            saved_count = self.save_results(parsed_results, db)
            
            # Update job status
            if job_id:
                job = db.query(ScraperJob).filter(ScraperJob.id == job_id).first()
                if job:
                    job.status = "success"
                    job.completedAt = datetime.now()
                    job.resultsCount = saved_count
                    job.executionTimeMs = int((datetime.now() - start_time).total_seconds() * 1000)
                    db.commit()
            
            self.logger.info("Scrape completed successfully", 
                           results_count=len(parsed_results),
                           saved_count=saved_count)
            
            return {
                "status": "success",
                "slug": self.slug,
                "results_found": len(parsed_results),
                "results_saved": saved_count,
                "execution_time_ms": int((datetime.now() - start_time).total_seconds() * 1000)
            }
            
        except Exception as e:
            self.logger.error("Scrape failed", error=str(e), exc_info=True)
            
            # Update job status to failed
            if job_id:
                try:
                    job = db.query(ScraperJob).filter(ScraperJob.id == job_id).first()
                    if job:
                        job.status = "failed"
                        job.completedAt = datetime.now()
                        job.errorMessage = str(e)
                        job.executionTimeMs = int((datetime.now() - start_time).total_seconds() * 1000)
                        db.commit()
                except Exception as db_error:
                    self.logger.error("Failed to update job status", error=str(db_error))
            
            return {
                "status": "failed",
                "slug": self.slug,
                "error": str(e),
                "execution_time_ms": int((datetime.now() - start_time).total_seconds() * 1000)
            }
        finally:
            db.close()
