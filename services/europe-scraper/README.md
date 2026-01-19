# Europe Lottery Scraper

A comprehensive Python-based lottery scraping service for European countries, featuring CRON scheduling, database integration, and a RESTful API.

## Features

- **Pan-European Coverage**: Supports 21+ lottery configurations across 19 European countries
- **CRON Scheduling**: Automated scraping with configurable schedules via APScheduler
- **Database Integration**: PostgreSQL database with SQLAlchemy ORM
- **RESTful API**: FastAPI-based API for monitoring and manual triggering
- **Flexible Scraping**: Both BeautifulSoup4 and Selenium support for different website types
- **Job Tracking**: Complete execution history and error tracking

## Supported Lotteries

### Pan-European
- EuroMillions (9 countries)
- EuroJackpot (18 countries)

### Major Countries
- 🇬🇧 United Kingdom: National Lottery, Thunderball
- 🇫🇷 France: Loto
- 🇪🇸 Spain: La Primitiva, Bonoloto, El Gordo
- 🇮🇹 Italy: SuperEnalotto, Million Day
- 🇩🇪 Germany: Lotto 6aus49
- 🇵🇱 Poland: Lotto, Multi Multi
- And 13 more countries...

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (recommended)

### Installation

1. **Clone the repository**
```bash
cd /Users/kvivek/Documents/global_lottery_platform/services/europe-scraper
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

The API will be available at `http://localhost:8001`

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

## Configuration

### CRON Schedules

Edit `src/config/countries.py` to modify scraper schedules:

```python
{
    "name": "UK National Lottery",
    "slug": "uk-national-lottery",
    "schedule": "0 21 * * 3,6",  # Wed, Sat 9 PM UTC
}
```

### Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SELENIUM_HEADLESS` - Run Selenium in headless mode (default: true)
- `SELENIUM_TIMEOUT` - Selenium timeout in seconds (default: 30)
- `LOG_LEVEL` - Logging level (INFO, DEBUG, WARNING, ERROR)

## Architecture

```
europe-scraper/
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
├── alembic/              # Database migrations
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Adding New Scrapers

1. **Add lottery configuration** in `src/config/countries.py`:
```python
{
    "name": "New Lottery",
    "slug": "country-lottery",
    "url": "https://example.com/results",
    "type": "selenium",  # or "bs4"
    "schedule": "0 20 * * 6",
}
```

2. **Create scraper class** in `src/scrapers/countries/country.py`:
```python
from src.scrapers.base.selenium_scraper import SeleniumScraper

class NewLotteryScraper(SeleniumScraper):
    def parse_results(self, driver):
        # Implement parsing logic
        return []
```

3. **Register scraper** in `src/scrapers/__init__.py`:
```python
from src.scrapers.countries.country import NewLotteryScraper

SCRAPER_REGISTRY = {
    "country-lottery": NewLotteryScraper,
}
```

## Testing

Run tests with pytest:
```bash
poetry run pytest
```

Run with coverage:
```bash
poetry run pytest --cov=src tests/
```

## Development

### Code Quality

Format code:
```bash
poetry run black src/
```

Lint code:
```bash
poetry run flake8 src/
```

Type check:
```bash
poetry run mypy src/
```

## Deployment

### Production Checklist

- [ ] Update `API_SECRET_KEY` in production
- [ ] Configure Sentry DSN for error tracking
- [ ] Set `SELENIUM_HEADLESS=true`
- [ ] Configure database backups
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure rate limiting per website
- [ ] Review and test all scraper schedules

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

## License

Proprietary - Internal use only

## Support

For issues or questions, contact the development team.
