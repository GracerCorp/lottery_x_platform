from datetime import datetime
from src.scrapers import get_scraper_by_slug
from src.database.session import get_db
from src.database.models import ScraperJob, Result, Lottery
from src.utils.logger import get_logger

logger = get_logger(__name__)


def transform_to_result_format(scraped_result):
    """
    Transform ScrapedResult to match existing database schema
    
    Converts:
    - winning_numbers (list) + bonus_numbers (list) -> numbers (JSON)
    - jackpot (dict) -> jackpot (text) + currency (text)
    """
    # Transform numbers to JSONB format
    numbers_data = {
        "main": scraped_result.winning_numbers,
        "bonus": scraped_result.bonus_numbers or []
    }
    
    # Format jackpot as text (e.g., "$100M", "€50M")
    jackpot_text = None
    currency = "USD"
    
    if scraped_result.jackpot:
        amount = scraped_result.jackpot.get('amount', 0)
        currency = scraped_result.jackpot.get('currency', 'USD')
        
        # Format large numbers with M/B suffix
        if amount >= 1_000_000:
            formatted_amount = f"{amount / 1_000_000:.1f}M"
        elif amount >= 1_000:
            formatted_amount = f"{amount / 1_000:.1f}K"
        else:
            formatted_amount = f"{amount:.0f}"
        
        # Add currency symbol
        currency_symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥',
            'SGD': 'S$', 'HKD': 'HK$', 'INR': '₹', 'KRW': '₩',
            'THB': '฿', 'PHP': '₱', 'MYR': 'RM', 'VND': '₫'
        }
        symbol = currency_symbols.get(currency, currency + ' ')
        jackpot_text = f"{symbol}{formatted_amount}"
    
    # Transform winners data if available
    winners_data = None
    if scraped_result.winners_count:
        winners_data = [
            {
                "tier": 1,
                "count": scraped_result.winners_count,
                "prize": scraped_result.jackpot.get('amount') if scraped_result.jackpot else None
            }
        ]
    
    return {
        "numbers": numbers_data,
        "jackpot": jackpot_text,
        "currency": currency,
        "winners": winners_data
    }


async def run_scraper(slug: str):
    """Execute a scraper by slug and save to database"""
    start_time = datetime.now()
    logger.info(f"Starting scraper", slug=slug)
    
    # Get lottery from database by slug
    with get_db() as db:
        lottery = db.query(Lottery).filter_by(slug=slug).first()
        if not lottery:
            logger.error(f"Lottery not found", slug=slug)
            return
        
        if not lottery.isActive:
            logger.info(f"Lottery is inactive", slug=slug)
            return
        
        lottery_id = lottery.id
        
        # Create job record
        job = ScraperJob(
            lotteryId=lottery_id,
            status='running',
            startedAt=start_time
        )
        db.add(job)
        db.commit()
        job_id = job.id
    
    try:
        # Get scraper instance
        scraper = get_scraper_by_slug(slug)
        if not scraper:
            raise Exception(f"No scraper found for slug: {slug}")
        
        # Execute scraper
        results = await scraper.execute()
        
        # Save results to database
        saved_count = 0
        with get_db() as db:
            for scraped_result in results:
                try:
                    # Check for duplicates
                    existing = db.query(Result).filter_by(
                        lotteryId=lottery_id,
                        drawDate=scraped_result.draw_date
                    ).first()
                    
                    if existing:
                        logger.debug(f"Result already exists", date=scraped_result.draw_date)
                        continue
                    
                    # Transform data to match schema
                    result_data = transform_to_result_format(scraped_result)
                    
                    # Create result record
                    db_result = Result(
                        lotteryId=lottery_id,
                        drawDate=scraped_result.draw_date,
                        numbers=result_data['numbers'],
                        jackpot=result_data['jackpot'],
                        currency=result_data['currency'],
                        winners=result_data['winners']
                    )
                    db.add(db_result)
                    saved_count += 1
                
                except Exception as e:
                    logger.error(f"Failed to save result", error=str(e))
            
            db.commit()
        
        # Update job as successful
        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
        with get_db() as db:
            job = db.query(ScraperJob).get(job_id)
            job.status = 'success'
            job.completedAt = datetime.now()
            job.resultsCount = saved_count
            job.executionTimeMs = execution_time
            db.commit()
        
        logger.info(
            f"Scraper completed successfully",
            slug=slug,
            saved=saved_count,
            execution_ms=execution_time
        )
        
    except Exception as e:
        logger.error(f"Scraper failed", slug=slug, error=str(e), exc_info=True)
        
        # Update job as failed
        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
        with get_db() as db:
            job = db.query(ScraperJob).get(job_id)
            job.status = 'failed'
            job.completedAt = datetime.now()
            job.errorMessage = str(e)
            job.executionTimeMs = execution_time
            db.commit()
        
        raise
