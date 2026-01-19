# North America Lottery Scraper

A comprehensive Python-based lottery scraping service for North American countries, featuring CRON scheduling, database integration, and a RESTful API.

## Features

- **North America Coverage**: Supports 50+ lottery configurations across 23 North American countries
- **CRON Scheduling**: Automated scraping with fully configurable schedules via APScheduler
- **Database Integration**: PostgreSQL database with SQLAlchemy ORM
- **RESTful API**: FastAPI-based API for monitoring and manual triggering
- **Flexible Scraping**: Both BeautifulSoup4 and Selenium support for different website types
- **Job Tracking**: Complete execution history and error tracking

## Supported Lotteries

### Major Markets
- 🇺🇸 **United States**: Powerball, Mega Millions
- 🇨🇦 **Canada**: Lotto 6/49, Lotto Max
- 🇲🇽 **Mexico**: Melate, Chispazo

### Caribbean Countries
- 🇯🇲 Jamaica: Supreme Ventures Lotto, Cash Pot
- 🇩🇴 Dominican Republic: Leidsa, Loteka
- 🇹🇹 Trinidad & Tobago: Play Whe, Lotto Plus
- And 10+ more Caribbean nations

### Central America
- 🇨🇷 Costa Rica, 🇵🇦 Panama, 🇬🇹 Guatemala
- 🇸🇻 El Salvador, 🇭🇳 Honduras, 🇳🇮 Nicaragua
- And more...

Total: **23 countries, 50+ lottery games**

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (recommended)

### Installation

1. **Clone the repository**
```bash
cd /Users/kvivek/Documents/global_lottery_platform/services/northamerica-scraper
```

2. **Install dependencies**
```bash
poetry install
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Initialize database**
```bash
poetry run python -m src.database.populate_lotteries
```

5. **Run the scraper**
```bash
poetry run python -m src.main
```

### Docker Deployment

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8002`

## API Endpoints

- `GET /` - Service information
- `GET /health` - Health check
- `GET /scrapers` - List all scrapers
- `GET /scrapers/{slug}` - Get scraper details
- `POST /scrapers/{slug}/run` - Manually trigger a scraper
- `GET /jobs` - List recent jobs
- `GET /jobs/{id}` - Get job details
- `GET /schedule` - View scheduled jobs
- `GET /lotteries` - List all lotteries

### Example API Calls

```bash
# Service info
curl http://localhost:8002/

# List all scrapers
curl http://localhost:8002/scrapers

# Trigger Powerball scraper
curl -X POST http://localhost:8002/scrapers/us-powerball/run

# Check recent jobs
curl http://localhost:8002/jobs

# View schedule
curl http://localhost:8002/schedule
```

## Configuration

### CRON Schedules

Edit `src/config/countries.py` to modify scraper schedules. All times are in UTC.

```python
{
    "name": "Powerball",
    "slug": "us-powerball",
    "schedule": "59 3 * * 2,4,7",  # Mon/Wed/Sat 10:59 PM ET = 3:59 AM UTC
}
```

CRON format: `minute hour day month day_of_week`

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://lottery_user:lottery_pass@localhost:5433/lottery_db

# Redis
REDIS_URL=redis://localhost:6380/0

# API
API_PORT=8002
API_SECRET_KEY=your-secret-key

# Selenium
SELENIUM_HEADLESS=true
SELENIUM_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
```

## Architecture

```
northamerica-scraper/
├── src/
│   ├── api/              # FastAPI application
│   ├── config/           # Configuration & country definitions
│   ├── database/         # Database models & session
│   ├── scrapers/         # Scraper implementations
│   │   ├── base/         # Base scraper classes
│   │   └── countries/    # Country-specific scrapers
│   ├── services/         # Scheduler & orchestrator
│   └── utils/            # Helper utilities
├── tests/                # Test suite
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Adding New Scrapers

### 1. Add Lottery Configuration

In `src/config/countries.py`:

```python
{
    "name": "New Lottery",
    "slug": "country-lottery",
    "url": "https://lottery-site.com/results",
    "type": "selenium",  # or "bs4"
    "schedule": "0 20 * * 6",  # CRON expression
}
```

### 2. Create Scraper Class

In `src/scrapers/countries/country.py`:

```python
from src.scrapers.base.selenium_scraper import SeleniumScraper

class NewLotteryScraper(SeleniumScraper):
    def parse_results(self, driver):
        # Implement parsing logic
        return [{
            "draw_date": datetime(...),
            "numbers": {"main": [1,2,3,4,5], "bonus": [6]},
            "jackpot": "$1M",
            "currency": "USD"
        }]
```

### 3. Register Scraper

In `src/scrapers/__init__.py`:

```python
from src.scrapers.countries.country import NewLotteryScraper

SCRAPER_REGISTRY = {
    "country-lottery": NewLotteryScraper,
}
```

## Testing

Run tests:
```bash
poetry run pytest
```

Run with coverage:
```bash
poetry run pytest --cov=src tests/
```

Code quality:
```bash
# Format
poetry run black src/

# Lint
poetry run flake8 src/

# Type check
poetry run mypy src/
```

## Deployment

### Production Checklist

- [ ] Update `API_SECRET_KEY` in production
- [ ] Configure Sentry DSN for error tracking
- [ ] Set `SELENIUM_HEADLESS=true`
- [ ] Configure database backups
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Review and test all scraper schedules
- [ ] Configure rate limiting per website

## Troubleshooting

### Selenium Issues
- Ensure Chrome/Chromium is installed in Docker container
- Check ChromeDriver compatibility with Chrome version
- Increase `SELENIUM_TIMEOUT` if pages load slowly

### Database Connection
- Verify PostgreSQL is running and accessible
- Check database credentials in `.env`
- Ensure database exists and tables are created

### Scraper Failures
- Check website structure hasn't changed
- Review error logs in `GET /jobs` API
- Test manually with `POST /scrapers/{slug}/run`

### CRON Not Triggering
- Verify scheduler is started (check logs)
- Confirm CRON expressions are valid
- Check timezone settings (all times should be UTC)

## Development

### Project Structure

- **Base Scrapers**: Reused from europe-scraper for consistency
- **Country Scrapers**: Custom implementations per lottery
- **Scheduler**: APScheduler with SQLAlchemy job store
- **Database**: Shared schema with europe-scraper
- **API**: FastAPI for RESTful interface

### Currently Implemented

✅ US: Powerball, Mega Millions  
✅ Canada: Lotto 6/49, Lotto Max  
✅ Mexico: Melate, Chispazo  

🚧 Remaining: 40+ lotteries across Caribbean and Central America

### Contributing

1. Implement new scrapers following the pattern above
2. Add tests for parsing logic
3. Update CRON schedules based on official draw times
4. Document any special handling or edge cases

## License

Proprietary - Internal use only

## Support

For issues or questions, contact the development team.

---

**Status**: ✅ Foundation Complete | 🚧 Scrapers In Progress  
**Version**: 1.0.0  
**Region**: North America (23 countries)
