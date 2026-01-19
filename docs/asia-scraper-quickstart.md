# Asia Lottery Scraper - Quick Start

## Installation

```bash
cd services/asia-scraper

# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Copy environment file
cp .env.example .env
```

## Configuration

Edit `.env`:

```bash
DATABASE_URL=postgresql://lottery_user:lottery_pass@localhost:5432/asia_lottery
REDIS_URL=redis://localhost:6379/0
API_SECRET_KEY=your-secret-key-here
```

## Running with Docker (Recommended)

```bash
# Start all services (PostgreSQL, Redis, Scraper)
docker-compose up -d

# View logs
docker-compose logs -f scraper

# Stop services
docker-compose down
```

The API will be available at `http://localhost:8000`

## Running Locally

```bash
# Initialize database
poetry run python -c "from src.database.session import init_db; init_db()"

# Start scraper service
poetry run python -m src.main
```

## API Usage

### Health Check
```bash
curl http://localhost:8000/health
```

### Trigger Manual Scrape
```bash
curl -X POST http://localhost:8000/scrape/sg-toto
```

### View Recent Jobs
```bash
curl http://localhost:8000/jobs?limit=20
```

### Get All Lotteries
```bash
curl http://localhost:8000/lotteries
```

## Available Scrapers

| Country | Lottery | Slug | Schedule |
|---------|---------|------|----------|
| 🇮🇳 India | Kerala State | `in-kerala-lottery` | Daily 4 PM IST |
| 🇮🇳 India | Sikkim State | `in-sikkim-lottery` | Daily 4 PM IST |
| 🇸🇬 Singapore | TOTO | `sg-toto` | Mon, Thu 7 PM SGT |
| 🇸🇬 Singapore | 4D | `sg-4d` | Wed, Sat, Sun 7 PM SGT |
| 🇲🇾 Malaysia | Magnum 4D | `my-magnum-4d` | Wed, Sat, Sun 7 PM MYT |
| 🇲🇾 Malaysia | Sports TOTO | `my-sports-toto` | Wed, Sat, Sun 7 PM MYT |
| 🇹🇭 Thailand | Government Lottery | `th-government-lottery` | 1st, 16th of month |
| 🇵🇭 Philippines | PCSO Lotto | `ph-pcso-lotto` | Daily 9 PM PHT |
| 🇯🇵 Japan | Takarakuji | `jp-takarakuji` | Mon, Thu 6 PM JST |
| 🇰🇷 South Korea | Lotto 6/45 | `kr-lotto-645` | Saturday 8 PM KST |
| 🇹🇼 Taiwan | Welfare Lottery | `tw-welfare-lottery` | Mon, Thu 8 PM CST |
| 🇭🇰 Hong Kong | Mark Six | `hk-mark-six` | Tue, Thu, Sat 9 PM HKT |
| 🇻🇳 Vietnam | Vietlott | `vn-vietlott` | Tue, Thu, Sat 6 PM ICT |

## Development

```bash
# Run tests
poetry run pytest

# Format code
poetry run black src/

# Type checking
poetry run mypy src/

# Start development server with auto-reload
poetry run uvicorn src.api.main:app --reload
```

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres
```

### Selenium/Chrome Issues
```bash
# Install Chrome/Chromium
# macOS
brew install --cask chromium

# Check driver path
which chromedriver
```

## Next Steps

1. Customize scraper implementations for specific lottery sites
2. Add more Asian countries
3. Set up monitoring and alerts
4. Deploy to production (Railway/VPS)
