# Europe Scraper - Quick Start Guide

Get the Europe Lottery Scraper up and running in **5 minutes** with Docker, or **10 minutes** with local development setup.

## Prerequisites

Choose your deployment method:

### Option A: Docker (Recommended)
- ✅ Docker Desktop or Docker Engine
- ✅ Docker Compose
- ✅ 4GB RAM minimum
- ✅ 10GB disk space

### Option B: Local Development
- ✅ Python 3.11 or higher
- ✅ PostgreSQL 16+
- ✅ Redis 7+
- ✅ Chrome/Chromium browser
- ✅ Poetry

---

## Quick Start with Docker (5 minutes)

### Step 1: Navigate to Project

```bash
cd /Users/kvivek/Documents/global_lottery_platform/services/europe-scraper
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# (Optional) Edit .env if you need custom settings
# Default values work out of the box!
```

### Step 3: Start Everything

```bash
# Build and start all services (PostgreSQL, Redis, Scraper)
docker-compose up --build
```

**What's happening:**
- 🐘 PostgreSQL starts on port `5432`
- 🔴 Redis starts on port `6379`
- 🐍 Europe Scraper API starts on port `8001`
- 📊 Database tables are created automatically
- ⏰ Scheduler loads 21 lottery configurations

### Step 4: Verify It's Running

Open a new terminal and test the API:

```bash
# Health check
curl http://localhost:8001/health

# Expected output:
# {"status":"healthy","environment":"development"}

# List all scrapers
curl http://localhost:8001/scrapers | jq

# Expected output:
# {"count":21,"scrapers":["uk-national-lottery","uk-thunderball",...]}
```

### Step 5: Populate Lottery Metadata

```bash
# Initialize European lottery data in database
docker exec -it europe-lottery-scraper poetry run python src/database/populate_lotteries.py
```

**Expected output:**
```
INFO: Added new lottery slug=uk-national-lottery
INFO: Added new lottery slug=fr-loto
...
INFO: Lottery population complete added=21 total=21
```

### Step 6: Test Your First Scrape

```bash
# Manually trigger UK National Lottery scraper
curl -X POST http://localhost:8001/scrapers/uk-national-lottery/run | jq

# Expected output:
# {
#   "status": "success",
#   "slug": "uk-national-lottery",
#   "results_found": 5,
#   "results_saved": 3,
#   "execution_time_ms": 8450
# }
```

### Step 7: View Results

```bash
# Check recent jobs
curl http://localhost:8001/jobs | jq '.jobs[] | {lottery_id, status, results_count}'

# Check scheduled jobs (CRON)
curl http://localhost:8001/schedule | jq
```

**🎉 You're done!** The scraper is now running and will automatically scrape lotteries based on their CRON schedules.

---

## Quick Start with Local Development (10 minutes)

### Step 1: Install Dependencies

```bash
cd /Users/kvivek/Documents/global_lottery_platform/services/europe-scraper

# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### Step 2: Set Up PostgreSQL

```bash
# Start PostgreSQL (if not running)
# macOS with Homebrew:
brew services start postgresql@16

# Create database
createdb lottery_db

# Or with psql:
psql -c "CREATE DATABASE lottery_db;"
```

### Step 3: Set Up Redis

```bash
# Start Redis (if not running)
# macOS with Homebrew:
brew services start redis

# Verify Redis is running
redis-cli ping
# Expected: PONG
```

### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your local database credentials
# Example:
# DATABASE_URL=postgresql://your_user:your_password@localhost:5432/lottery_db
# REDIS_URL=redis://localhost:6379/0
```

### Step 5: Initialize Database

```bash
# Create tables
poetry run python -c "from src.database.session import init_db; init_db()"

# Populate lottery metadata
poetry run python src/database/populate_lotteries.py
```

### Step 6: Install Chrome/ChromeDriver (for Selenium)

```bash
# macOS with Homebrew:
brew install --cask google-chrome
brew install chromedriver

# Verify installation
chromedriver --version
```

### Step 7: Run the Scraper

```bash
# Start the service
poetry run python -m src.main
```

**Expected output:**
```
INFO: === Europe Lottery Scraper Starting ===
INFO: Initializing database
INFO: Database initialized
INFO: Scheduler started
INFO: Loading scrapers
INFO: Loaded scraper slug=uk-national-lottery cron='0 21 * * 3,6'
...
INFO: Scrapers loaded count=21
INFO: Starting API server port=8001
INFO: Uvicorn running on http://0.0.0.0:8001
```

### Step 8: Test (in another terminal)

```bash
# Test API
curl http://localhost:8001/health

# Trigger a scrape
curl -X POST http://localhost:8001/scrapers/es-primitiva/run | jq
```

---

## Understanding the Output

### Successful Scrape

```json
{
  "status": "success",
  "slug": "uk-national-lottery",
  "results_found": 5,
  "results_saved": 3,
  "execution_time_ms": 8450
}
```

**Meaning:**
- ✅ Scraper ran successfully
- 📊 Found 5 draw results on the website
- 💾 Saved 3 new results to database (2 were duplicates)
- ⏱️ Took 8.45 seconds

### Failed Scrape

```json
{
  "status": "failed",
  "slug": "uk-national-lottery",
  "error": "Timeout waiting for element",
  "execution_time_ms": 30500
}
```

**Meaning:**
- ❌ Scraper failed
- 📝 Error details provided
- 🔍 Check logs for more info

---

## Monitoring Your Scrapers

### View All Scrapers

```bash
curl http://localhost:8001/scrapers | jq '.scrapers[]'
```

### Check Scraper Details

```bash
curl http://localhost:8001/scrapers/uk-national-lottery | jq
```

**Output:**
```json
{
  "slug": "uk-national-lottery",
  "name": "UK National Lottery",
  "country": "United Kingdom",
  "url": "https://www.national-lottery.co.uk/results/lotto",
  "type": "selenium",
  "schedule": "0 21 * * 3,6"
}
```

### View Job History

```bash
# Last 50 jobs
curl http://localhost:8001/jobs | jq

# Filter by status
curl http://localhost:8001/jobs | jq '.jobs[] | select(.status=="success")'
curl http://localhost:8001/jobs | jq '.jobs[] | select(.status=="failed")'
```

### View Scheduled Jobs

```bash
# See when scrapers will run next
curl http://localhost:8001/schedule | jq
```

**Output:**
```json
{
  "count": 21,
  "jobs": [
    {
      "id": "scraper_uk-national-lottery",
      "name": "run_scraper",
      "next_run": "2026-01-22T21:00:00+00:00"
    },
    ...
  ]
}
```

---

## Testing Individual Scrapers

### UK National Lottery

```bash
curl -X POST http://localhost:8001/scrapers/uk-national-lottery/run | jq
```

### Spain La Primitiva (BeautifulSoup)

```bash
curl -X POST http://localhost:8001/scrapers/es-primitiva/run | jq
```

### EuroMillions (Pan-European)

```bash
curl -X POST http://localhost:8001/scrapers/eu-euromillions/run | jq
```

---

## Verifying Database Integration

### Connect to PostgreSQL

```bash
# Using Docker
docker exec -it europe-lottery-postgres psql -U lottery_user -d lottery_db

# Using local PostgreSQL
psql -U your_user -d lottery_db
```

### Check Lotteries

```sql
-- View European lotteries
SELECT slug, name, country, "isActive"
FROM lottery
WHERE region = 'Europe'
ORDER BY country;

-- Expected: 21 rows
```

### Check Results

```sql
-- View recent results
SELECT 
    l.name,
    r."drawDate",
    r.numbers,
    r.jackpot,
    r.currency
FROM lottery l
JOIN result r ON l.id = r."lotteryId"
WHERE l.region = 'Europe'
ORDER BY r."drawDate" DESC
LIMIT 10;
```

### Check Scraper Jobs

```sql
-- View job execution history
SELECT 
    l.slug,
    j.status,
    j."resultsCount",
    j."executionTimeMs",
    j."startedAt"
FROM scraper_job j
JOIN lottery l ON j."lotteryId" = l.id
ORDER BY j."startedAt" DESC
LIMIT 10;
```

---

## Common Issues & Solutions

### Issue: Port 8001 already in use

```bash
# Find process using port 8001
lsof -i :8001

# Kill process
kill -9 <PID>

# Or change port in .env
echo "API_PORT=8002" >> .env
```

### Issue: Database connection refused

```bash
# Check PostgreSQL is running
docker ps | grep postgres
# OR
pg_isadmin

# Verify DATABASE_URL in .env
cat .env | grep DATABASE_URL
```

### Issue: ChromeDriver not found

```bash
# Docker: Rebuild image
docker-compose build scraper

# Local: Install ChromeDriver
brew install chromedriver
```

### Issue: Scraper timeout

```env
# Increase timeout in .env
SELENIUM_TIMEOUT=60
```

### Issue: No results saved

**Possible reasons:**
1. ✅ Scraper logic needs adjustment (website changed)
2. ✅ All results already exist (duplicates)
3. ✅ Lottery is not active (`isActive = false`)

**Debug:**
```bash
# Check scraper logs
docker-compose logs -f scraper

# Check job details
curl http://localhost:8001/jobs | jq '.jobs[0]'
```

---

## Stopping the Service

### Docker

```bash
# Stop services
docker-compose down

# Stop and remove volumes (clears database!)
docker-compose down -v
```

### Local Development

```bash
# Press Ctrl+C in the terminal running the scraper

# Stop PostgreSQL
brew services stop postgresql@16

# Stop Redis
brew services stop redis
```

---

## Next Steps

1. ✅ **Integration**: Connect with Next.js frontend ([europe-scraper-integration.md](./europe-scraper-integration.md))
2. ✅ **Add Scrapers**: Implement more country scrapers ([europe-scraper.md](./europe-scraper.md#adding-new-scrapers))
3. ✅ **Production**: Deploy to production environment
4. ✅ **Monitoring**: Set up Sentry for error tracking
5. ✅ **Scheduling**: Review and adjust CRON schedules

---

## Useful Commands Cheat Sheet

```bash
# Docker Management
docker-compose up -d                    # Start in background
docker-compose logs -f scraper          # Follow logs
docker-compose restart scraper          # Restart scraper
docker exec -it europe-lottery-scraper bash  # Shell into container

# API Testing
curl http://localhost:8001/health                           # Health check
curl http://localhost:8001/scrapers                         # List scrapers
curl -X POST http://localhost:8001/scrapers/{slug}/run      # Trigger scrape
curl http://localhost:8001/jobs                             # Job history
curl http://localhost:8001/schedule                         # CRON schedule

# Database
docker exec -it europe-lottery-postgres psql -U lottery_user -d lottery_db
poetry run python src/database/populate_lotteries.py        # Re-populate

# Development
poetry install                                              # Install deps
poetry run pytest                                           # Run tests
poetry run black src/                                       # Format code
poetry run python -m src.main                               # Run locally
```

---

## Support

**Logs:**
```bash
# Docker
docker-compose logs -f scraper

# Local
# Logs are output to stdout/stderr
```

**Documentation:**
- Full documentation: [europe-scraper.md](./europe-scraper.md)
- Integration guide: [europe-scraper-integration.md](./europe-scraper-integration.md)

**Troubleshooting:**
1. Check `/jobs` endpoint for errors
2. Review Docker logs
3. Verify database connectivity
4. Test individual scrapers manually
