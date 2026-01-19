"""FastAPI application for Europe lottery scraper"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from src.config.settings import settings
from src.services.scheduler import get_scheduled_jobs
from src.services.orchestrator import run_scraper
from src.scrapers import get_all_scraper_slugs
from src.database.session import get_db
from src.database.models import ScraperJob, Lottery
from src.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Europe Lottery Scraper API",
    description="API for managing European lottery scrapers",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Europe Lottery Scraper",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }


@app.get("/scrapers")
async def list_scrapers():
    """List all registered scrapers"""
    slugs = get_all_scraper_slugs()
    return {
        "count": len(slugs),
        "scrapers": slugs
    }


@app.get("/scrapers/{slug}")
async def get_scraper_info(slug: str):
    """Get information about a specific scraper"""
    from src.config.countries import get_lottery_config
    
    config = get_lottery_config(slug)
    if not config:
        raise HTTPException(status_code=404, detail=f"Scraper '{slug}' not found")
    
    return {
        "slug": slug,
        "name": config["name"],
        "country": config["country_name"],
        "url": config["url"],
        "type": config["type"],
        "schedule": config["schedule"]
    }


@app.post("/scrapers/{slug}/run")
async def trigger_scraper(slug: str):
    """Manually trigger a scraper"""
    logger.info("Manual scraper trigger", slug=slug)
    
    try:
        result = run_scraper(slug)
        return result
    except Exception as e:
        logger.error("Failed to run scraper", slug=slug, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs")
async def list_jobs(limit: int = 50):
    """List recent scraper jobs"""
    db = get_db()
    try:
        jobs = db.query(ScraperJob).order_by(ScraperJob.createdAt.desc()).limit(limit).all()
        
        return {
            "count": len(jobs),
            "jobs": [
                {
                    "id": job.id,
                    "lottery_id": str(job.lotteryId),
                    "status": job.status,
                    "started_at": job.startedAt.isoformat() if job.startedAt else None,
                    "completed_at": job.completedAt.isoformat() if job.completedAt else None,
                    "results_count": job.resultsCount,
                    "execution_time_ms": job.executionTimeMs,
                    "error": job.errorMessage
                }
                for job in jobs
            ]
        }
    finally:
        db.close()


@app.get("/jobs/{job_id}")
async def get_job(job_id: int):
    """Get details of a specific job"""
    db = get_db()
    try:
        job = db.query(ScraperJob).filter(ScraperJob.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
        
        return {
            "id": job.id,
            "lottery_id": str(job.lotteryId),
            "status": job.status,
            "started_at": job.startedAt.isoformat() if job.startedAt else None,
            "completed_at": job.completedAt.isoformat() if job.completedAt else None,
            "results_count": job.resultsCount,
            "execution_time_ms": job.executionTimeMs,
            "error": job.errorMessage
        }
    finally:
        db.close()


@app.get("/schedule")
async def get_schedule():
    """Get scheduled jobs"""
    jobs = get_scheduled_jobs()
    
    return {
        "count": len(jobs),
        "jobs": [
            {
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None
            }
            for job in jobs
        ]
    }


@app.get("/lotteries")
async def list_lotteries(active_only: bool = True):
    """List all lotteries in database"""
    db = get_db()
    try:
        query = db.query(Lottery)
        if active_only:
            query = query.filter(Lottery.isActive == True)
        
        lotteries = query.all()
        
        return {
            "count": len(lotteries),
            "lotteries": [
                {
                    "id": str(lottery.id),
                    "name": lottery.name,
                    "slug": lottery.slug,
                    "country": lottery.country,
                    "is_active": lottery.isActive
                }
                for lottery in lotteries
            ]
        }
    finally:
        db.close()
