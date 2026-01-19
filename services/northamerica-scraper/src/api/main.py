"""FastAPI application for North America lottery scraper"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from src.config.settings import settings
from src.config.countries import get_all_lottery_slugs, get_lottery_config, ALL_COUNTRIES
from src.services.orchestrator import run_scraper
from src.services.scheduler import get_scheduled_jobs
from src.database.session import get_db
from src.database.models import Lottery, ScraperJob
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="North America Lottery Scraper API",
    description="RESTful API for North American lottery scraping service",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.API_ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> Dict:
    """Service information"""
    return {
        "service": "North America Lottery Scraper",
        "version": "1.0.0",
        "region": "North America",
        "countries": len(ALL_COUNTRIES),
        "lotteries": len(get_all_lottery_slugs()),
    }


@app.get("/health")
def health_check() -> Dict:
    """Health check endpoint"""
    db = get_db()
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        db_status = "unhealthy"
    finally:
        db.close()
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": db_status,
        "api": "healthy",
    }


@app.get("/scrapers")
def list_scrapers() -> List[Dict]:
    """List all available scrapers"""
    slugs = get_all_lottery_slugs()
    scrapers = []
    
    for slug in slugs:
        config = get_lottery_config(slug)
        if config:
            scrapers.append({
                "slug": slug,
                "name": config["name"],
                "country": config["country_name"],
                "url": config["url"],
                "type": config["type"],
                "schedule": config["schedule"],
            })
    
    return scrapers


@app.get("/scrapers/{slug}")
def get_scraper(slug: str) -> Dict:
    """Get scraper details by slug"""
    config = get_lottery_config(slug)
    if not config:
        raise HTTPException(status_code=404, detail=f"Scraper not found: {slug}")
    
    return config


@app.post("/scrapers/{slug}/run")
def trigger_scraper(slug: str) -> Dict:
    """Manually trigger a scraper"""
    config = get_lottery_config(slug)
    if not config:
        raise HTTPException(status_code=404, detail=f"Scraper not found: {slug}")
    
    logger.info("Manual scraper trigger", slug=slug)
    result = run_scraper(slug)
    return result


@app.get("/jobs")
def list_jobs(limit: int = 50) -> List[Dict]:
    """List recent scraper jobs"""
    db = get_db()
    try:
        jobs = db.query(ScraperJob).order_by(ScraperJob.createdAt.desc()).limit(limit).all()
        return [
            {
                "id": job.id,
                "lottery_id": str(job.lotteryId),
                "status": job.status,
                "started_at": job.startedAt.isoformat() if job.startedAt else None,
                "completed_at": job.completedAt.isoformat() if job.completedAt else None,
                "results_count": job.resultsCount,
                "execution_time_ms": job.executionTimeMs,
                "error_message": job.errorMessage,
            }
            for job in jobs
        ]
    finally:
        db.close()


@app.get("/jobs/{job_id}")
def get_job(job_id: int) -> Dict:
    """Get job details by ID"""
    db = get_db()
    try:
        job = db.query(ScraperJob).filter(ScraperJob.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail=f"Job not found: {job_id}")
        
        return {
            "id": job.id,
            "lottery_id": str(job.lotteryId),
            "status": job.status,
            "started_at": job.startedAt.isoformat() if job.startedAt else None,
            "completed_at": job.completedAt.isoformat() if job.completedAt else None,
            "results_count": job.resultsCount,
            "execution_time_ms": job.executionTimeMs,
            "error_message": job.errorMessage,
        }
    finally:
        db.close()


@app.get("/schedule")
def get_schedule() -> List[Dict]:
    """View scheduled jobs"""
    jobs = get_scheduled_jobs()
    return [
        {
            "id": job.id,
            "name": job.name,
            "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger),
        }
        for job in jobs
    ]


@app.get("/lotteries")
def list_lotteries() -> List[Dict]:
    """List all North American lotteries"""
    db = get_db()
    try:
        lotteries = db.query(Lottery).filter(Lottery.region == "North America").all()
        return [
            {
                "id": str(lottery.id),
                "name": lottery.name,
                "slug": lottery.slug,
                "country": lottery.country,
                "region": lottery.region,
                "is_active": lottery.isActive,
                "official_link": lottery.officialLink,
            }
            for lottery in lotteries
        ]
    finally:
        db.close()


@app.get("/lotteries/{slug}")
def get_lottery(slug: str) -> Dict:
    """Get lottery details by slug"""
    db = get_db()
    try:
        lottery = db.query(Lottery).filter(Lottery.slug == slug).first()
        if not lottery:
            raise HTTPException(status_code=404, detail=f"Lottery not found: {slug}")
        
        return {
            "id": str(lottery.id),
            "name": lottery.name,
            "slug": lottery.slug,
            "country": lottery.country,
            "region": lottery.region,
            "is_active": lottery.isActive,
            "official_link": lottery.officialLink,
            "description": lottery.description,
            "frequency": lottery.frequency,
        }
    finally:
        db.close()
