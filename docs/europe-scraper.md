# Europe Lottery Scraper

## Overview

The **Europe Lottery Scraper** is a comprehensive Python-based microservice that automatically scrapes lottery results from **21+ lottery configurations across 19 European countries**. Built using the same architecture as the Asia scraper, it features CRON-based scheduling, database integration, and a RESTful API for monitoring and control.

## Key Features

- 🌍 **Pan-European Coverage**: EuroMillions, EuroJackpot, and major national lotteries
- ⏰ **CRON Scheduling**: APScheduler with configurable schedules per lottery
- 💾 **Database Integration**: Shares the same PostgreSQL schema with Next.js and Asia scraper
- 🚀 **FastAPI REST API**: Monitoring, manual triggering, and job tracking on port 8001
- 🤖 **Flexible Scraping**: BeautifulSoup4 for static sites, Selenium for JavaScript-heavy sites
- 📊 **Job Tracking**: Complete execution history and error tracking in `scraper_job` table
- 🐳 **Docker Ready**: Full containerization with docker-compose

## Supported Lotteries

### Pan-European (2 lotteries)
- **EuroMillions** - 9 participating countries (Tue, Fri 9 PM UTC)
- **EuroJackpot** - 18 participating countries (Tue, Fri 8 PM UTC)

### Major Countries (19 countries, 21 configurations)

| Country | Lotteries | Scraper Type | Schedule |
|---------|-----------|--------------|----------|
| 🇬🇧 United Kingdom | National Lottery, Thunderball | Selenium | Wed/Sat, Tue/Wed/Fri/Sat |
| 🇫🇷 France | Loto | Selenium | Mon/Wed/Sat |
| 🇪🇸 Spain | La Primitiva, Bonoloto, El Gordo | BS4 | Mon/Thu/Sat, Daily, Sunday |
| 🇮🇹 Italy | SuperEnalotto, Million Day | Selenium, BS4 | Tue/Thu/Sat, Daily |
| 🇩🇪 Germany | Lotto 6aus49 | Selenium | Wed/Sat |
| 🇵🇱 Poland | Lotto, Multi Multi | Selenium | Tue/Thu/Sat, Daily |
| 🇳🇱 Netherlands | Staatsloterij | Selenium | Monthly (10th) |
| 🇧🇪 Belgium | Lotto Belgium | Selenium | Wed/Sat |
| 🇸🇪 Sweden | Svenska Spel Lotto | Selenium | Saturday |
| 🇳🇴 Norway | Norsk Tipping Lotto | Selenium | Saturday |
| 🇩🇰 Denmark | Lotto Denmark | Selenium | Saturday |
| 🇫🇮 Finland | Veikkaus Lotto | Selenium | Saturday |
| 🇦🇹 Austria | Lotto Austria | Selenium | Wed/Sat |
| 🇨🇭 Switzerland | Swiss Loto | Selenium | Wed/Sat |
| 🇵🇹 Portugal | Euromilhões Portugal | Selenium | Tue/Fri |
| 🇬🇷 Greece | OPAP Lotto | Selenium | Wed/Sat |
| 🇨🇿 Czech Republic | Sportka | Selenium | Wed/Sat |
| 🇮🇪 Ireland | Irish Lotto | Selenium | Wed/Sat |
| 🇭🇺 Hungary | Hatoslottó | Selenium | Sunday |

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────┐
│         Europe Lottery Scraper (Port 8001)          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌────────────┐      ┌──────────────┐              │
│  │  FastAPI   │      │  APScheduler │              │
│  │   Server   │      │   (CRON)     │              │
│  └─────┬──────┘      └──────┬───────┘              │
│        │                    │                       │
│        └────────┬───────────┘                       │
│                 ▼                                   │
│         ┌──────────────┐                            │
│         │ Orchestrator │                            │
│         └──────┬───────┘                            │
│                │                                    │
│       ┌────────┴────────┐                           │
│       ▼                 ▼                           │
│  ┌─────────┐      ┌──────────┐                     │
│  │   BS4   │      │ Selenium │                     │
│  │ Scraper │      │ Scraper  │                     │
│  └────┬────┘      └─────┬────┘                     │
│       └────────┬─────────┘                          │
│                ▼                                    │
│         Country Scrapers                            │
│  (UK, FR, ES, IT, DE, PL, NL, ...)                 │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
         ┌────────────────┐
         │   PostgreSQL   │
         │   (Shared DB)  │
         └────────────────┘
                  ▲
                  │
  ┌───────────────┼───────────────┐
  │               │               │
Asia Scraper   Next.js App   Europe Scraper
```

### Tech Stack

- **Python 3.11+** - Modern async/await support
- **SQLAlchemy 2.0** - ORM with UUID support
- **APScheduler 3.10** - CRON job scheduling with SQLAlchemy job store
- **FastAPI** - High-performance async API framework
- **Uvicorn** - ASGI server
- **Selenium 4** - Browser automation with Chrome WebDriver
- **BeautifulSoup4 + lxml** - HTML parsing
- **httpx** - Async HTTP client
- **Redis 7** - Caching and rate limiting
- **Poetry** - Dependency management
- **Docker + Docker Compose** - Containerization

## Project Structure

```
services/europe-scraper/
├── src/
│   ├── api/
│   │   └── main.py                    # FastAPI application (port 8001)
│   ├── config/
│   │   ├── countries.py               # 21 lottery configurations
│   │   └── settings.py                # Pydantic settings
│   ├── database/
│   │   ├── models.py                  # SQLAlchemy models (Lottery, Result, ScraperJob)
│   │   ├── session.py                 # Database session management
│   │   └── populate_lotteries.py      # Seed European lotteries
│   ├── scrapers/
│   │   ├── __init__.py                # Scraper registry
│   │   ├── base/
│   │   │   ├── base_scraper.py        # Abstract base class
│   │   │   ├── bs4_scraper.py         # BeautifulSoup4 scraper
│   │   │   └── selenium_scraper.py    # Selenium scraper
│   │   └── countries/
│   │       ├── uk.py                  # UK National Lottery, Thunderball
│   │       ├── spain.py               # La Primitiva, Bonoloto, El Gordo
│   │       └── ...                    # Other country scrapers
│   ├── services/
│   │   ├── scheduler.py               # APScheduler CRON integration
│   │   └── orchestrator.py            # Scraper execution logic
│   ├── utils/
│   │   ├── logger.py                  # Structured logging (structlog)
│   │   └── helpers.py                 # European date/number parsing
│   └── main.py                        # Application entry point
├── tests/
│   └── test_basic.py                  # Unit tests
├── docs/
│   └── README.md                      # Full documentation
├── docker-compose.yml                 # PostgreSQL, Redis, Scraper
├── Dockerfile                         # Multi-stage build with Chrome
├── pyproject.toml                     # Poetry dependencies
├── pytest.ini                         # Test configuration
├── .env.example                       # Environment template
└── .gitignore
```

## API Endpoints

### Service Management

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/` | GET | Service information | `{"service": "Europe Lottery Scraper", "version": "1.0.0"}` |
| `/health` | GET | Health check | `{"status": "healthy", "environment": "production"}` |

### Scraper Management

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/scrapers` | GET | List all registered scrapers | Returns 21 scraper slugs |
| `/scrapers/{slug}` | GET | Get scraper details | Schedule, URL, country info |
| `/scrapers/{slug}/run` | POST | Manually trigger a scraper | Immediate execution |

### Job Monitoring

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/jobs` | GET | List recent jobs (limit=50) | Job history with status |
| `/jobs/{id}` | GET | Get job details | Execution time, results count, errors |
| `/schedule` | GET | View scheduled jobs | Next run times |

### Data Access

| Endpoint | Method | Description | Example |
|----------|--------|-------------|---------|
| `/lotteries` | GET | List all lotteries | Filter by `active_only=true` |

## Database Schema

### Shared Tables (Used by Europe Scraper, Asia Scraper, Next.js)

#### `lottery` Table
```sql
CREATE TABLE lottery (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    country TEXT NOT NULL,
    region TEXT,
    frequency TEXT,
    logo TEXT,
    description TEXT,
    "officialLink" TEXT,
    "isActive" BOOLEAN DEFAULT true,
    "createdAt" TIMESTAMP DEFAULT now(),
    "updatedAt" TIMESTAMP DEFAULT now()
);
```

**Europe Scraper Responsibility**: Populated by `populate_lotteries.py` with 21 European lottery configurations.

#### `result` Table
```sql
CREATE TABLE result (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "lotteryId" UUID REFERENCES lottery(id),
    "drawDate" TIMESTAMP NOT NULL,
    numbers JSONB NOT NULL,              -- {"main": [1,2,3], "bonus": [4]}
    jackpot TEXT,                        -- "€100M"
    currency TEXT DEFAULT 'EUR',
    winners JSONB,                       -- [{"tier": 1, "prize": 1000000, "count": 1}]
    "createdAt" TIMESTAMP DEFAULT now(),
    UNIQUE("lotteryId", "drawDate")      -- Prevent duplicates
);
```

**Europe Scraper Responsibility**: Writes draw results with automatic deduplication.

### Scraper-Specific Tables

#### `scraper_job` Table
```sql
CREATE TABLE scraper_job (
    id SERIAL PRIMARY KEY,
    "lotteryId" UUID REFERENCES lottery(id),
    status VARCHAR(20) NOT NULL,         -- 'pending', 'running', 'success', 'failed'
    "startedAt" TIMESTAMP,
    "completedAt" TIMESTAMP,
    "errorMessage" TEXT,
    "resultsCount" INTEGER DEFAULT 0,
    "executionTimeMs" INTEGER,
    "createdAt" TIMESTAMP DEFAULT now()
);
```

#### `scraper_config` Table
```sql
CREATE TABLE scraper_config (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    "updatedAt" TIMESTAMP DEFAULT now()
);
```

## Configuration

### Environment Variables

```bash
# Database (shared with Next.js and Asia scraper)
DATABASE_URL=postgresql://lottery_user:lottery_pass@localhost:5432/lottery_db

# Redis (caching and rate limiting)
REDIS_URL=redis://localhost:6379/0

# API Configuration
API_SECRET_KEY=your-secret-key-change-in-production
API_PORT=8001

# Selenium Configuration
SELENIUM_HEADLESS=true
SELENIUM_TIMEOUT=30

# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_PERIOD=60

# Logging
LOG_LEVEL=INFO

# Sentry (optional)
SENTRY_DSN=

# Environment
ENVIRONMENT=production
```

### CRON Schedules

Configured in `src/config/countries.py`:

```python
{
    "name": "UK National Lottery",
    "slug": "uk-national-lottery",
    "url": "https://www.national-lottery.co.uk/results/lotto",
    "type": "selenium",
    "schedule": "0 21 * * 3,6",  # Wednesday, Saturday at 9 PM UTC
}
```

**CRON Format**: `minute hour day month day_of_week`

Examples:
- `0 21 * * 3,6` - Wednesday & Saturday at 9 PM UTC
- `0 19 * * *` - Daily at 7 PM UTC
- `0 20 10 * *` - 10th of every month at 8 PM UTC

## Data Flow

```
1. APScheduler triggers scraper based on CRON schedule
   ↓
2. Orchestrator calls scraper by slug
   ↓
3. Scraper fetches page (BS4 or Selenium)
   ↓
4. Parser extracts draw data
   ↓
5. Database save with deduplication
   ↓
6. ScraperJob record updated (success/failed)
   ↓
7. Next.js API reads results from `result` table
   ↓
8. Frontend displays results
```

## Adding New Scrapers

### Step 1: Add Configuration

Edit `src/config/countries.py`:

```python
CountryConfig(
    code="XX",
    name="Country Name",
    timezone="Europe/City",
    lotteries=[
        {
            "name": "Lottery Name",
            "slug": "country-lottery-slug",
            "url": "https://example.com/results",
            "type": "selenium",  # or "bs4"
            "schedule": "0 20 * * 6",  # CRON expression
        }
    ]
)
```

### Step 2: Implement Scraper

Create `src/scrapers/countries/country.py`:

```python
from src.scrapers.base.selenium_scraper import SeleniumScraper
from src.utils.helpers import parse_european_date

class CountryLotteryScraper(SeleniumScraper):
    def parse_results(self, driver):
        results = []
        
        # Wait for results to load
        self.wait_for_element(By.CLASS_NAME, "results")
        
        # Extract data
        elements = driver.find_elements(By.CLASS_NAME, "draw")
        
        for elem in elements:
            draw_date = parse_european_date(elem.find_element(By.CLASS_NAME, "date").text)
            numbers = [int(ball.text) for ball in elem.find_elements(By.CLASS_NAME, "ball")]
            
            results.append({
                "draw_date": draw_date,
                "numbers": {"main": sorted(numbers[:6]), "bonus": numbers[6:]},
                "currency": "EUR"
            })
        
        return results
```

### Step 3: Register Scraper

Edit `src/scrapers/__init__.py`:

```python
from src.scrapers.countries.country import CountryLotteryScraper

SCRAPER_REGISTRY = {
    "country-lottery-slug": CountryLotteryScraper,
    # ... other scrapers
}
```

### Step 4: Test

```bash
# Populate lottery metadata
poetry run python src/database/populate_lotteries.py

# Test manually
curl -X POST http://localhost:8001/scrapers/country-lottery-slug/run

# Check results
curl http://localhost:8001/jobs
```

## Utilities

### European Date Parsing

```python
from src.utils.helpers import parse_european_date

date = parse_european_date("25/12/2024")  # DD/MM/YYYY
date = parse_european_date("25-12-2024")  # DD-MM-YYYY
date = parse_european_date("25.12.2024")  # DD.MM.YYYY
```

### European Number Parsing

```python
from src.utils.helpers import parse_european_number

amount = parse_european_number("1.234.567,89")  # Returns 1234567.89
amount = parse_european_number("1 234 567,89")  # Returns 1234567.89
```

### Currency Parsing

```python
from src.utils.helpers import parse_currency

amount, currency = parse_currency("€100M")      # (100000000, "EUR")
amount, currency = parse_currency("£50,000")    # (50000, "GBP")
amount, currency = parse_currency("CHF 1.5M")   # (1500000, "CHF")
```

## Troubleshooting

### Selenium Issues

**Problem**: ChromeDriver not found
```bash
# Ensure Chrome is installed in Docker
docker exec -it europe-lottery-scraper google-chrome --version
```

**Problem**: Page timeout
```env
# Increase timeout
SELENIUM_TIMEOUT=60
```

### Database Connection

**Problem**: Connection refused
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Verify connection string
psql $DATABASE_URL -c "SELECT version();"
```

### Scraper Failures

**Problem**: Website structure changed

1. Check error logs:
```bash
curl http://localhost:8001/jobs | jq '.jobs[] | select(.status=="failed")'
```

2. Test manually:
```bash
curl -X POST http://localhost:8001/scrapers/uk-national-lottery/run
```

3. Review HTML structure and update selectors

## Performance & Monitoring

### Metrics

- **Execution time**: Tracked in `scraper_job.executionTimeMs`
- **Success rate**: `COUNT(status='success') / COUNT(*)`
- **Results per scraper**: `scraper_job.resultsCount`

### Logging

Structured logging with `structlog`:

```python
logger.info("Scraping started", slug="uk-national-lottery", url="https://...")
logger.error("Scraping failed", error=str(e), exc_info=True)
```

### Error Tracking

Integrate Sentry for production:

```env
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project
```

## Deployment

See [europe-scraper-quickstart.md](./europe-scraper-quickstart.md) for detailed deployment instructions.

## Integration

See [europe-scraper-integration.md](./europe-scraper-integration.md) for database integration with Next.js and Asia scraper.

## Support

For issues or questions:
- Check logs: `docker-compose logs -f scraper`
- Review job history: `GET /jobs`
- Test individual scrapers: `POST /scrapers/{slug}/run`
