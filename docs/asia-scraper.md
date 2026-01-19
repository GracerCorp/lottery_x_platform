# Asia Lottery Scraper (Python)

Python-based lottery scraper for Asian countries with configurable CRON scheduling and PostgreSQL storage.

## Features

- 🌏 **10+ Asian Countries**: India, Singapore, Malaysia, Thailand, Philippines, Japan, South Korea, Taiwan, Hong Kong, Vietnam
- ⏰ **APScheduler**: Database-backed CRON scheduling
- 🐍 **Python 3.11+**: Modern async/await support
- 💾 **PostgreSQL**: SQLAlchemy ORM with migration support
- 🔍 **Multi-Strategy Scraping**: BeautifulSoup, Selenium, API clients
- 🎯 **Pydantic Validation**: Type-safe data models
- 🚀 **FastAPI**: Modern REST API
- 🔒 **Production Ready**: Docker, structured logging, error tracking

## Quick Start

### Prerequisites

- Python 3.11+
- Poetry
- PostgreSQL
- Redis
- Chrome/Chromium (for Selenium)

### Installation

```bash
cd services/asia-scraper

# Install dependencies with Poetry
poetry install

# Copy environment file
cp .env.example .env
# Edit .env with your database credentials

# Initialize database
poetry run python -c "from src.database.session import init_db; init_db()"
```

### Running with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f scraper

# Stop services
docker-compose down
```

### Running Locally

```bash
# Start the scraper service
poetry run python -m src.main

# Or use the CLI
poetry run scraper
```

## Project Structure

```
src/
├── config/          # Settings and country configs
├── scrapers/        # Scraper implementations
│   ├── base/       # Base classes (BS4, Selenium)
│   └── countries/  # Country-specific scrapers
├── services/        # Scheduler, orchestrator
├── database/        # SQLAlchemy models
├── api/            # FastAPI endpoints
├── utils/          # Logger, helpers
└── main.py         # Entry point
```

## API Endpoints

Once running, access the API at `http://localhost:8000`

- `GET /` - Service info
- `GET /health` - Health check
- `GET /config` - Get scheduler config
- `PUT /config` - Update config
- `POST /scrape/{slug}` - Trigger manual scrape
- `GET /jobs` - Recent jobs
- `GET /lotteries` - All lotteries
- `GET /scheduler/jobs` - Scheduled jobs

## Supported Lotteries

### India
- Kerala State Lottery
- Sikkim State Lottery

### Singapore
- TOTO
- 4D

### Malaysia
- Magnum 4D
- Sports TOTO

### Thailand
- Government Lottery

### Philippines
- PCSO Lotto

### Japan
- Takarakuji

### South Korea
- Lotto 6/45

### Taiwan
- Public Welfare Lottery

### Hong Kong
- Mark Six

### Vietnam
- Vietlott

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run specific test file
poetry run pytest tests/test_india_scrapers.py

# Run tests matching pattern
poetry run pytest -k "scraper_registry"

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Use the test runner script
poetry run python run_tests.py
```

### Test Structure

```
tests/
├── test_base_scraper.py        # Base scraper tests
├── test_scraper_registry.py    # Registry integration tests
├── test_india_scrapers.py      # India scraper tests
├── test_singapore_scrapers.py  # Singapore scraper tests
├── test_scheduler.py           # Scheduler tests
└── __init__.py
```

### Code Quality

```bash
# Run tests
poetry run pytest

# Format code
poetry run black src/

# Type checking
poetry run mypy src/

# Lint
poetry run flake8 src/
```

## Configuration

Edit `.env` file:

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/asia_lottery
REDIS_URL=redis://localhost:6379/0
API_SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
MAX_CONCURRENT_SCRAPERS=3
```

## Deployment

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway up
```

### VPS

```bash
# Build and run with Docker
docker-compose -f docker-compose.prod.yml up -d
```

## License

MIT
