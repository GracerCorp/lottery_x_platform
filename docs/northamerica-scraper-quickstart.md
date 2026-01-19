# North America Lottery Scraper - Quick Start Guide

Get the **North America Lottery Scraper** up and running in **5 minutes**.

---

## Prerequisites

Before starting, ensure you have:

- ✅ **Docker** and **Docker Compose** installed
- ✅ **Python 3.11+** (for local development)
- ✅ **Poetry** (Python dependency manager)
- ✅ **PostgreSQL 16+** (or use Docker)
- ✅ **Git** (to clone the repository)

---

## Option 1: Docker Deployment (Recommended)

### Step 1: Navigate to Service Directory

```bash
cd /Users/kvivek/Documents/global_lottery_platform/services/northamerica-scraper
```

### Step 2: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# (Optional) Edit configuration
# vim .env
```

**Default Configuration:**
```bash
DATABASE_URL=postgresql://lottery_user:lottery_pass@postgres:5432/lottery_db
REDIS_URL=redis://redis:6379/0
API_PORT=8002
SELENIUM_HEADLESS=true
LOG_LEVEL=INFO
```

### Step 3: Start Services

```bash
# Build and start all services (PostgreSQL, Redis, Scraper)
docker-compose up --build -d
```

**Expected Output:**
```
Creating network "northamerica-scraper_default"
Creating northamerica-lottery-postgres ... done
Creating northamerica-lottery-redis    ... done
Creating northamerica-lottery-scraper  ... done
```

### Step 4: Check Service Health

```bash
# View logs
docker-compose logs -f scraper

# Health check
curl http://localhost:8002/health
```

**Expected Response:**
```json
{
    "status": "healthy",
    "database": "healthy",
    "api": "healthy"
}
```

### Step 5: Initialize Database

```bash
# Create scraper_job and scraper_config tables
docker exec -it northamerica-lottery-scraper poetry run python -c "from src.database.session import init_db; init_db()"

# Populate North American lotteries
docker exec -it northamerica-lottery-scraper poetry run python src/database/populate_lotteries.py
```

**Expected Output:**
```
INFO: Added new lottery slug=us-powerball
INFO: Added new lottery slug=us-megamillions
INFO: Added new lottery slug=ca-lotto649
...
INFO: Lottery population complete added=50 updated=0 total=50
```

### Step 6: Verify Setup

```bash
# Check service info
curl http://localhost:8002/

# List all scrapers
curl http://localhost:8002/scrapers | jq

# View schedule
curl http://localhost:8002/schedule | jq
```

### Step 7: Test a Scraper

```bash
# Manually trigger Powerball scraper
curl -X POST http://localhost:8002/scrapers/us-powerball/run

# Check job status
curl http://localhost:8002/jobs | jq
```

**Success!** 🎉 The North America scraper is now running and will automatically scrape on schedule.

---

## Option 2: Local Development

### Step 1: Install Dependencies

```bash
cd /Users/kvivek/Documents/global_lottery_platform/services/northamerica-scraper

# Install Poetry (if not installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

### Step 2: Start PostgreSQL and Redis

**Option A: Use Docker for just databases**
```bash
# Start only PostgreSQL and Redis from docker-compose
docker-compose up -d postgres redis
```

**Option B: Use local PostgreSQL**
```bash
# Create database
createdb lottery_db

# Create user (if needed)
psql -c "CREATE USER lottery_user WITH PASSWORD 'lottery_pass';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE lottery_db TO lottery_user;"
```

### Step 3: Configure Environment

```bash
cp .env.example .env

# Edit for local development
vim .env
```

**Local Configuration:**
```bash
DATABASE_URL=postgresql://lottery_user:lottery_pass@localhost:5433/lottery_db
REDIS_URL=redis://localhost:6380/0
API_PORT=8002
SELENIUM_HEADLESS=false  # Set to false to see browser during development
LOG_LEVEL=DEBUG
```

### Step 4: Initialize Database

```bash
# Create tables
poetry run python -c "from src.database.session import init_db; init_db()"

# Populate lotteries
poetry run python src/database/populate_lotteries.py
```

### Step 5: Install Chrome/ChromeDriver (for Selenium)

**macOS:**
```bash
# Install Chrome
brew install --cask google-chrome

# Install ChromeDriver
brew install chromedriver
```

### Step 6: Run the Scraper

```bash
# Start the service
poetry run python -m src.main
```

**Expected Output:**
```
INFO: === North America Lottery Scraper Starting ===
INFO: Initializing database
INFO: Database initialized
INFO: Scheduler started
INFO: Loading scrapers
INFO: Loaded scraper slug=us-powerball cron=59 3 * * 2,4,7
INFO: Loaded scraper slug=us-megamillions cron=0 4 * * 3,6
...
INFO: Scrapers loaded count=50
INFO: Starting API server port=8002
INFO: Uvicorn running on http://0.0.0.0:8002
```

### Step 7: Test API

```bash
# In another terminal

# Service info
curl http://localhost:8002/

# List scrapers
curl http://localhost:8002/scrapers | jq

# Trigger Powerball
curl -X POST http://localhost:8002/scrapers/us-powerball/run
```

---

## Quick Commands Reference

### Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f scraper

# Restart scraper only
docker-compose restart scraper

# Rebuild after code changes
docker-compose up --build -d

# Access scraper container
docker exec -it northamerica-lottery-scraper bash
```

### Database Commands

```bash
# Connect to PostgreSQL
docker exec -it northamerica-lottery-postgres psql -U lottery_user -d lottery_db

# Check North American lotteries
psql $DATABASE_URL -c "SELECT slug, name, country FROM lottery WHERE region = 'North America';"

# Check recent results
psql $DATABASE_URL -c "SELECT l.name, r.\"drawDate\", r.jackpot FROM result r JOIN lottery l ON r.\"lotteryId\" = l.id WHERE l.region = 'North America' ORDER BY r.\"drawDate\" DESC LIMIT 5;"

# Check scraper jobs
psql $DATABASE_URL -c "SELECT l.name, j.status, j.\"startedAt\", j.\"resultsCount\" FROM scraper_job j JOIN lottery l ON j.\"lotteryId\" = l.id WHERE l.region = 'North America' ORDER BY j.\"startedAt\" DESC LIMIT 10;"
```

### API Commands

```bash
# Service health
curl http://localhost:8002/health

# List all scrapers
curl http://localhost:8002/scrapers

# Get specific scraper
curl http://localhost:8002/scrapers/us-powerball

# Trigger scraper
curl -X POST http://localhost:8002/scrapers/us-powerball/run

# List recent jobs
curl http://localhost:8002/jobs

# Get job details
curl http://localhost:8002/jobs/1

# View schedule
curl http://localhost:8002/schedule

# List all lotteries
curl http://localhost:8002/lotteries

# Get specific lottery
curl http://localhost:8002/lotteries/us-powerball
```

---

## Testing Your Setup

### Test 1: Verify Database Population

```bash
# Count North American lotteries
curl http://localhost:8002/lotteries | jq 'length'
# Expected: 50+
```

### Test 2: Manually Run a Scraper

```bash
# Trigger Powerball scraper
curl -X POST http://localhost:8002/scrapers/us-powerball/run | jq

# Expected response:
# {
#   "status": "success",
#   "slug": "us-powerball",
#   "results_found": 5,
#   "results_saved": 5,
#   "execution_time_ms": 15000
# }
```

### Test 3: Verify Results Saved

```bash
# Check results via API
curl http://localhost:8002/lotteries | jq '.[] | select(.slug=="us-powerball")'

# Check results in database
docker exec -it northamerica-lottery-postgres psql -U lottery_user -d lottery_db -c \
  "SELECT * FROM result WHERE \"lotteryId\" IN (SELECT id FROM lottery WHERE slug = 'us-powerball') ORDER BY \"drawDate\" DESC LIMIT 1;"
```

### Test 4: Check Scheduler

```bash
# View scheduled jobs
curl http://localhost:8002/schedule | jq

# Expected: List of jobs with next_run_time
```

---

## Integration with Next.js

### Verify North American Lotteries Appear in Next.js

```bash
# Check if Next.js can see North American lotteries
curl http://localhost:3000/api/lotteries | jq '.[] | select(.region=="North America")'

# Expected: Should show Powerball, Mega Millions, etc.
```

### Frontend Display

The scraped results are immediately available to the Next.js frontend via the shared database:

```typescript
// Frontend automatically shows North American lotteries
// No additional configuration needed!

// Example query:
const lotteries = await db
  .select()
  .from(lottery)
  .where(eq(lottery.region, 'North America'));
```

---

## Troubleshooting

### Issue: Service Won't Start

**Check Docker:**
```bash
docker-compose ps
docker-compose logs scraper
```

**Common Solutions:**
- Ensure ports 8002, 5433, 6380 are not in use
- Check `.env` file exists
- Run `docker-compose down -v` and restart

### Issue: Database Connection Errors

**Check PostgreSQL:**
```bash
docker-compose logs postgres

# Test connection
docker exec -it northamerica-lottery-postgres psql -U lottery_user -d lottery_db -c "SELECT 1;"
```

**Solution:**
- Wait for PostgreSQL health check to pass
- Verify `DATABASE_URL` in `.env`

### Issue: Scraper Fails

**Check Logs:**
```bash
docker-compose logs -f scraper

# Or check jobs API
curl http://localhost:8002/jobs | jq '.[] | select(.status=="failed")'
```

**Common Causes:**
- Website structure changed → Update scraper parser
- Selenium timeout → Increase `SELENIUM_TIMEOUT` in `.env`
- Network issues → Check internet connection

### Issue: No Results Saved

**Check:**
1. Did the scraper run successfully?
   ```bash
   curl http://localhost:8002/jobs | jq '.[-1]'
   ```

2. Are results being parsed?
   - Check scraper logs for parsing errors

3. Is deduplication blocking?
   - Results with same `lotteryId` + `drawDate` are skipped

### Issue: CRON Not Triggering

**Verify Scheduler:**
```bash
curl http://localhost:8002/schedule | jq
```

**Check:**
- Scheduler is started (check logs: "Scheduler started")
- CRON expressions are valid (5 parts: minute hour day month day_of_week)
- Times are in UTC

---

## Next Steps

✅ **Running Successfully?** Great! Now:

1. 📖 Read the [Integration Guide](./northamerica-scraper-integration.md) to understand database integration
2. 🔧 Configure CRON schedules for your timezone
3. 🌍 Add more country-specific scrapers (see [northamerica-scraper.md](./northamerica-scraper.md))
4. 📊 Set up monitoring and alerts
5. 🚀 Deploy to production

---

## Production Deployment Checklist

Before deploying to production:

- [ ] Update `API_SECRET_KEY` to a strong random value
- [ ] Set `SELENIUM_HEADLESS=true`
- [ ] Configure Sentry DSN for error tracking
- [ ] Set up database backups
- [ ] Configure monitoring (Prometheus/Grafana)
- [ ] Review CRON schedules for production draw times
- [ ] Test all scrapers manually
- [ ] Set up rate limiting per domain
- [ ] Configure proper logging (JSON format)
- [ ] Set resource limits in docker-compose.yml

---

## Support

**Need Help?**
- 📖 [Full Documentation](./northamerica-scraper.md)
- 🔗 [Integration Guide](./northamerica-scraper-integration.md)
- 🏗️ [Technical README](../services/northamerica-scraper/README.md)

**Still stuck?** Contact the development team.

---

**Quick Start Complete!** 🎉

Your North America Lottery Scraper is now scraping lottery results from 23 countries automatically. Results are stored in the shared database and immediately available to your Next.js application.
