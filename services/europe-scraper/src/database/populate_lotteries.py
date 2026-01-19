"""Initialize database with European lottery metadata"""

from sqlalchemy.exc import IntegrityError
from src.database.session import get_db
from src.database.models import Lottery
from src.config.countries import ALL_COUNTRIES
from src.utils.logger import get_logger

logger = get_logger(__name__)


def populate_lotteries():
    """Populate lottery table with European lottery configurations"""
    db = get_db()
    
    try:
        added_count = 0
        updated_count = 0
        
        for country in ALL_COUNTRIES:
            for lottery_config in country.lotteries:
                slug = lottery_config["slug"]
                
                # Check if lottery already exists
                existing = db.query(Lottery).filter(Lottery.slug == slug).first()
                
                if existing:
                    # Update existing lottery
                    existing.name = lottery_config["name"]
                    existing.country = country.name
                    existing.officialLink = lottery_config["url"]
                    existing.description = lottery_config.get("description", "")
                    existing.isActive = True
                    updated_count += 1
                    logger.info("Updated lottery", slug=slug)
                else:
                    # Create new lottery
                    new_lottery = Lottery(
                        name=lottery_config["name"],
                        slug=slug,
                        country=country.name,
                        region="Europe",
                        officialLink=lottery_config["url"],
                        description=lottery_config.get("description", ""),
                        isActive=True
                    )
                    db.add(new_lottery)
                    added_count += 1
                    logger.info("Added new lottery", slug=slug)
        
        db.commit()
        logger.info("Lottery population complete", 
                   added=added_count, 
                   updated=updated_count,
                   total=added_count + updated_count)
        
    except Exception as e:
        db.rollback()
        logger.error("Failed to populate lotteries", error=str(e))
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_lotteries()
