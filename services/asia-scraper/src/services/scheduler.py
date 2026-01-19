from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
from src.config.settings import settings
from src.utils.logger import get_logger
from src.services.orchestrator import run_scraper

logger = get_logger(__name__)

# Configure job store
jobstores = {
    'default': SQLAlchemyJobStore(url=settings.DATABASE_URL)
}

# Create scheduler
scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    timezone='UTC'
)


def parse_cron_expression(cron_expr: str) -> dict:
    """
    Parse cron expression to APScheduler kwargs
    Example: '0 16 * * *' -> {'hour': 16, 'minute': 0}
    """
    parts = cron_expr.split()
    if len(parts) != 5:
        raise ValueError(f"Invalid cron expression: {cron_expr}")
    
    minute, hour, day, month, day_of_week = parts
    
    kwargs = {}
    if minute != '*':
        kwargs['minute'] = minute
    if hour != '*':
        kwargs['hour'] = hour
    if day != '*':
        kwargs['day'] = day
    if month != '*':
        kwargs['month'] = month
    if day_of_week != '*':
        kwargs['day_of_week'] = day_of_week
    
    return kwargs


def schedule_scraper(slug: str, cron_expr: str):
    """Add scraper job to scheduler"""
    try:
        cron_kwargs = parse_cron_expression(cron_expr)
        trigger = CronTrigger(**cron_kwargs, timezone='UTC')
        
        scheduler.add_job(
            run_scraper,
            trigger=trigger,
            args=[slug],
            id=f'scraper_{slug}',
            replace_existing=True,
            max_instances=1
        )
        
        logger.info(f"Scheduled scraper", slug=slug, cron=cron_expr)
        
    except Exception as e:
        logger.error(f"Failed to schedule scraper", slug=slug, error=str(e))
        raise


def remove_scraper_job(slug: str):
    """Remove scraper job from scheduler"""
    job_id = f'scraper_{slug}'
    try:
        scheduler.remove_job(job_id)
        logger.info(f"Removed scraper job", slug=slug)
    except Exception as e:
        logger.warning(f"Failed to remove job", slug=slug, error=str(e))


def start_scheduler():
    """Start the APScheduler"""
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler started")


def stop_scheduler():
    """Stop the APScheduler"""
    if scheduler.running:
        scheduler.shutdown(wait=True)
        logger.info("Scheduler stopped")


def get_scheduled_jobs():
    """Get all scheduled jobs"""
    return scheduler.get_jobs()
