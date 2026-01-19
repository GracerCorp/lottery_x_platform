from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.session import get_db_session
from src.database.models import ScraperConfig, ScraperJob, Lottery
from src.services.scheduler import scheduler, get_scheduled_jobs
from src.services.orchestrator import run_scraper
from src.utils.logger import get_logger


logger = get_logger(__name__)

app = FastAPI(
    title="Asia Lottery Scraper API",
    description="REST API for managing Asian lottery scrapers",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Asia Lottery Scraper",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "scheduler_running": scheduler.running,
        "scheduled_jobs": len(get_scheduled_jobs())
    }


@app.get("/config")
async def get_config(db: Session = Depends(get_db_session)):
    """Get scheduler configuration"""
    config = db.query(ScraperConfig).filter_by(key='scheduler').first()
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config.value


@app.put("/config")
async def update_config(config_data: dict, db: Session = Depends(get_db_session)):
    """Update scheduler configuration"""
    config = db.query(ScraperConfig).filter_by(key='scheduler').first()
    if not config:
        config = ScraperConfig(key='scheduler', value=config_data)
        db.add(config)
    else:
        config.value = config_data
    
    db.commit()
    return {"success": True, "config": config.value}


@app.post("/scrape/{slug}")
async def trigger_scrape(slug: str):
    """Manually trigger a scraper"""
    try:
        # Use scheduler to run immediately
        scheduler.add_job(
            run_scraper,
            args=[slug],
            id=f'manual_{slug}',
            replace_existing=True
        )
        return {"success": True, "message": f"Scraper queued: {slug}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs")
async def get_jobs(
    limit: int = 50,
    db: Session = Depends(get_db_session)
):
    """Get recent scraper jobs"""
    jobs = db.query(ScraperJob).order_by(
        ScraperJob.created_at.desc()
    ).limit(limit).all()
    
    return {"jobs": [
        {
            "id": job.id,
            "lottery_id": job.lottery_id,
            "status": job.status,
            "started_at": job.started_at,
            "completed_at": job.completed_at,
            "results_count": job.results_count,
            "execution_time_ms": job.execution_time_ms,
            "error_message": job.error_message
        }
        for job in jobs
    ]}


@app.get("/lotteries")
async def get_lotteries(db: Session = Depends(get_db_session)):
    """Get all lotteries"""
    lotteries = db.query(Lottery).all()
    
    return {"lotteries": [
        {
            "id": str(lot.id),
            "name": lot.name,
            "slug": lot.slug,
            "country": lot.country,
            "isActive": lot.isActive,
        }
        for lot in lotteries
    ]}


@app.get("/scheduler/jobs")
async def get_scheduler_jobs():
    """Get all scheduled jobs"""
    jobs = get_scheduled_jobs()
    return {
        "jobs": [
            {
                "id": job.id,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger)
            }
            for job in jobs
        ]
    }
