"""
Populate Asian lotteries into the existing lottery table

This script adds Asian lottery configurations to the shared database,
making them accessible to both the Python scraper and Next.js frontend.
"""

import uuid
from src.config.countries import ASIAN_COUNTRIES
from src.database.models import Lottery
from src.database.session import get_db
from src.utils.logger import get_logger

logger = get_logger(__name__)


def cron_to_frequency(cron_expr: str) -> str:
    """
    Convert CRON expression to human-readable frequency
    
    Examples:
        "0 19 * * 1,4" -> "Mon, Thu"
        "0 21 * * 2,4,6" -> "Tue, Thu, Sat"
        "0 15 1,16 * *" -> "1st, 16th of month"
    """
    parts = cron_expr.split()
    if len(parts) != 5:
        return "Variable"
    
    _, _, day, _, day_of_week = parts
    
    # Check for specific days of week
    if day_of_week != '*':
        day_map = {
            '0': 'Sun', '1': 'Mon', '2': 'Tue', '3': 'Wed',
            '4': 'Thu', '5': 'Fri', '6': 'Sat'
        }
        days = [day_map.get(d, d) for d in day_of_week.split(',')]
        return ', '.join(days)
    
    # Check for specific days of month
    if day != '*':
        days = day.replace(',', ', ')
        if ',' in days:
            return f"{days} of month"
        return f"{day} of month"
    
    return "Daily"


def populate_asian_lotteries():
    """Populate lottery table with Asian lottery configurations"""
    
    logger.info("Starting lottery population")
    added_count = 0
    updated_count = 0
    
    try:
        with get_db() as db:
            for country_config in ASIAN_COUNTRIES:
                for lottery_config in country_config.lotteries:
                    slug = lottery_config['slug']
                    
                    # Check if lottery already exists
                    existing = db.query(Lottery).filter_by(slug=slug).first()
                    
                    if existing:
                        # Update existing lottery
                        existing.name = lottery_config['name']
                        existing.country = country_config.name
                        existing.region = 'Asia'
                        existing.frequency = cron_to_frequency(lottery_config['schedule'])
                        existing.officialLink = lottery_config['url']
                        existing.isActive = True
                        existing.updatedAt = func.now()
                        
                        updated_count += 1
                        logger.info(f"Updated lottery: {slug}")
                    else:
                        # Create new lottery
                        lottery = Lottery(
                            id=uuid.uuid4(),
                            name=lottery_config['name'],
                            slug=slug,
                            country=country_config.name,
                            region='Asia',
                            frequency=cron_to_frequency(lottery_config['schedule']),
                            officialLink=lottery_config['url'],
                            isActive=True,
                            description=f"{lottery_config['name']} from {country_config.name}"
                        )
                        db.add(lottery)
                        added_count += 1
                        logger.info(f"Added lottery: {slug}")
            
            db.commit()
        
        logger.info(
            f"Population complete",
            added=added_count,
            updated=updated_count,
            total=added_count + updated_count
        )
        
        print(f"✅ Successfully populated {added_count} new lotteries")
        print(f"✅ Updated {updated_count} existing lotteries")
        
    except Exception as e:
        logger.error(f"Population failed", error=str(e), exc_info=True)
        print(f"❌ Population failed: {e}")
        raise


# Run if called directly
if __name__ == "__main__":
    from src.database.session import init_db
    
    print("Initializing database...")
    init_db()
    
    print("\nPopulating Asian lotteries...")
    populate_asian_lotteries()
    
    print("\n✅ All done! Asian lotteries are now in the database.")
    print("You can view them in Drizzle Studio or via the Next.js API:")
    print("  curl http://localhost:3000/api/lotteries")
