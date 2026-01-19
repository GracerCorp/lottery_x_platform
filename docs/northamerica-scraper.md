# North America Lottery Scraper

> **Production-ready Python service for scraping lottery results from 23 North American countries with CRON scheduling, database integration, and RESTful API.**

## Quick Links

- 📖 [Integration Guide](./northamerica-scraper-integration.md) - Database integration with Next.js and other scrapers
- ⚡ [Quick Start](./northamerica-scraper-quickstart.md) - Get started in 5 minutes
- 🏗️ [Architecture](../services/northamerica-scraper/README.md) - Technical details

---

## Overview

The **North America Lottery Scraper** is a comprehensive Python-based service that automatically scrapes lottery results from **23 North American countries**, covering **50+ lottery games**. It integrates seamlessly with the existing global lottery platform, sharing the same PostgreSQL database with Europe and Asia scrapers.

### Key Features

✅ **Wide Geographic Coverage** - All 23 North American countries  
✅ **CRON Scheduling** - Fully configurable automated scraping via APScheduler  
✅ **Database Integration** - Shares PostgreSQL database with Next.js application  
✅ **RESTful API** - FastAPI with 12 endpoints for monitoring and control  
✅ **Dual Scraping Strategies** - Selenium for JavaScript-heavy sites, BeautifulSoup4 for static HTML  
✅ **Job Tracking** - Complete execution history with error logging  
✅ **Deduplication** - Prevents duplicate results automatically  

---

## Supported Lotteries

### Major Markets (6 Implemented)

#### 🇺🇸 United States
- **Powerball** - Mon/Wed/Sat at 10:59 PM ET
- **Mega Millions** - Tue/Fri at 11:00 PM ET

#### 🇨🇦 Canada
- **Lotto 6/49** - Wed/Sat at 9:30 PM ET
- **Lotto Max** - Tue/Fri at 9:30 PM ET

#### 🇲🇽 Mexico
- **Melate** - Wed/Sat/Sun at 9:00 PM CST
- **Chispazo** - Daily at 9:00 PM CST

### Caribbean Countries (16 Configured)

🇯🇲 Jamaica  
🇩🇴 Dominican Republic  
🇹🇹 Trinidad & Tobago  
🇭🇹 Haiti  
🇨🇺 Cuba  
🇧🇸 Bahamas  
🇧🇧 Barbados  
🇱🇨 Saint Lucia  
🇻🇨 Saint Vincent and the Grenadines  
🇬🇩 Grenada  
🇦🇬 Antigua and Barbuda  
🇰🇳 Saint Kitts and Nevis  
🇩🇲 Dominica  

**Lotteries:** Supreme Ventures Lotto, Cash Pot, Leidsa Quiniela, Loteka, NLCB Play Whe, Lotto Plus, and more

### Central America (6 Configured)

🇬🇹 Guatemala  
🇧🇿 Belize  
🇭🇳 Honduras  
🇸🇻 El Salvador  
🇳🇮 Nicaragua  
🇨🇷 Costa Rica  
🇵🇦 Panama  

**Lotteries:** National lotteries for each country

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────┐
│                PostgreSQL Database (Shared)              │
│                                                          │
│  ┌─────────┐  ┌────────┐  ┌─────────────┐             │
│  │ lottery │  │ result │  │ scraper_job │             │
│  └────┬────┘  └───┬────┘  └─────┬───────┘             │
└───────┼───────────┼─────────────┼────────────────────────┘
        │           │             │
   ┌────┴───────────┴─────────────┴────┐
   │                                    │
┌──┴────┐  ┌───────────┐  ┌────────────┴──┐
│Next.js│  │  Europe   │  │ North America │
│  App  │  │  Scraper  │  │   Scraper     │
│ :3000 │  │  :8001    │  │   :8002       │
└───────┘  └───────────┘  └───────────────┘
```

### Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.11+ |
| **Package Manager** | Poetry | Latest |
| **Database** | PostgreSQL | 16+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Cache** | Redis | 7+ |
| **Scheduler** | APScheduler | 3.10+ |
| **Web Framework** | FastAPI | 0.109+ |
| **Server** | Uvicorn | 0.27+ |
| **Scraping** | Selenium + BS4 | 4.16+ / 4.12+ |

### Service Components

```
northamerica-scraper/
├── src/
│   ├── api/              # FastAPI REST API (12 endpoints)
│   ├── config/           # Country configs (23 countries, 50+ lotteries)
│   ├── database/         # SQLAlchemy models (shared schema)
│   ├── scrapers/
│   │   ├── base/         # BaseScraper, SeleniumScraper, BS4Scraper
│   │   └── countries/    # USA, Canada, Mexico scrapers
│   ├── services/         # Scheduler + Orchestrator
│   └── utils/            # Validators + Logger
├── Dockerfile            # Multi-stage build with Chrome/ChromeDriver
└── docker-compose.yml    # PostgreSQL + Redis + Scraper
```

---

## Data Flow

### 1. Initial Setup

```
populate_lotteries.py
    ↓
Inserts 50+ North American lotteries into lottery table
    ↓
region='North America'
    ↓
Next.js API can query all lotteries
```

### 2. Scheduled Scraping

```
APScheduler triggers (e.g., Mon 3:59 AM UTC for Powerball)
    ↓
Orchestrator calls PowerballScraper
    ↓
Selenium loads powerball.com/previous-results
    ↓
Parser extracts: numbers, jackpot, draw date
    ↓
Saves to result table (with deduplication)
    ↓
Creates scraper_job record (success/failed)
    ↓
Next.js API shows new results immediately
```

### 3. Manual Triggering

```bash
curl -X POST http://localhost:8002/scrapers/us-powerball/run
    ↓
Same flow as scheduled scraping
    ↓
Returns execution summary JSON
```

---

## Database Schema

### Shared Tables (All Scrapers)

#### `lottery` Table

```sql
CREATE TABLE lottery (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,        -- e.g., 'us-powerball'
    country TEXT NOT NULL,             -- e.g., 'United States'
    region TEXT,                       -- 'North America'
    officialLink TEXT,
    description TEXT,
    isActive BOOLEAN DEFAULT true,
    createdAt TIMESTAMP DEFAULT now(),
    updatedAt TIMESTAMP DEFAULT now()
);
```

**North America Scraper Role:**
- ✍️ Writes 50+ North American lottery records via `populate_lotteries.py`
- 👁️ Reads lottery IDs for result insertion

#### `result` Table

```sql
CREATE TABLE result (
    id UUID PRIMARY KEY,
    lotteryId UUID REFERENCES lottery(id),
    drawDate TIMESTAMP NOT NULL,
    numbers JSONB NOT NULL,            -- {"main": [1,2,3], "bonus": [4]}
    jackpot TEXT,                      -- "$100M"
    currency TEXT,                     -- "USD", "CAD", "MXN"
    winners JSONB,
    createdAt TIMESTAMP DEFAULT now(),
    UNIQUE(lotteryId, drawDate)        -- Deduplication
);
```

**North America Scraper Role:**
- ✍️ Writes lottery result data
- Enforces deduplication via unique constraint

### Service-Specific Tables

#### `scraper_job` Table

```sql
CREATE TABLE scraper_job (
    id SERIAL PRIMARY KEY,
    lotteryId UUID REFERENCES lottery(id),
    status VARCHAR(20),                -- 'success', 'failed'
    startedAt TIMESTAMP,
    completedAt TIMESTAMP,
    resultsCount INTEGER DEFAULT 0,
    executionTimeMs INTEGER,
    errorMessage TEXT,
    createdAt TIMESTAMP DEFAULT now()
);
```

**Purpose:** Track every scraper execution for monitoring and debugging.

---

## Example Scraper Implementation

### Powerball Scraper

```python
class PowerballScraper(SeleniumScraper):
    """Scraper for US Powerball lottery"""
    
    def parse_results(self, driver) -> List[Dict]:
        # Wait for results to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "game-result"))
        )
        
        # Parse 5 main numbers (1-69) + 1 Powerball (1-26)
        results = []
        for element in driver.find_elements(By.CLASS_NAME, "game-result")[:5]:
            # Extract date, numbers, jackpot
            results.append({
                "draw_date": datetime(...),
                "numbers": {
                    "main": [5, 15, 25, 35, 45],  # Sorted
                    "bonus": [10]
                },
                "jackpot": "$100M",
                "currency": "USD"
            })
        
        return results
```

**Output Format (Standardized):**
```json
{
    "draw_date": "2024-01-15T00:00:00",
    "numbers": {
        "main": [5, 15, 25, 35, 45],
        "bonus": [10]
    },
    "jackpot": "$100M",
    "currency": "USD"
}
```

---

## API Endpoints

**Base URL:** `http://localhost:8002`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info (region, countries, lotteries count) |
| `/health` | GET | Health check (DB connectivity) |
| `/scrapers` | GET | List all 50+ scrapers with CRON schedules |
| `/scrapers/{slug}` | GET | Get scraper configuration |
| `/scrapers/{slug}/run` | POST | Manually trigger scraper |
| `/jobs` | GET | List recent job executions (limit 50) |
| `/jobs/{id}` | GET | Get job details  by ID |
| `/schedule` | GET | View scheduled jobs with next run times |
| `/lotteries` | GET | List all North America lotteries |
| `/lotteries/{slug}` | GET | Get lottery details |

### Example API Calls

```bash
# Service info
curl http://localhost:8002/

# List all scrapers
curl http://localhost:8002/scrapers | jq

# Trigger Powerball manually
curl -X POST http://localhost:8002/scrapers/us-powerball/run

# Check recent jobs
curl http://localhost:8002/jobs | jq

# View CRON schedule
curl http://localhost:8002/schedule | jq
```

---

## CRON Scheduling

All schedules configured in **UTC timezone** in `src/config/countries.py`:

```python
{
    "name": "Powerball",
    "slug": "us-powerball",
    "url": "https://www.powerball.com/previous-results",
    "type": "selenium",
    "schedule": "59 3 * * 2,4,7",  # Mon/Wed/Sat 10:59 PM ET = 3:59 AM UTC
}
```

**CRON Format:** `minute hour day month day_of_week`

**Timezone Conversion Examples:**
- Powerball: 10:59 PM ET → 3:59 AM UTC (next day)
- Lotto 6/49: 9:30 PM ET → 2:30 AM UTC (next day)
- Melate: 9:00 PM CST → 3:00 AM UTC (next day)

---

## Currency Support

**Supported Currencies:**

| Region | Currency | Code |
|--------|----------|------|
| United States | US Dollar | `USD` |
| Canada | Canadian Dollar | `CAD` |
| Mexico | Mexican Peso | `MXN` |
| Costa Rica | Costa Rican Colón | `CRC` |
| Panama | Panamanian Balboa | `PAB` |
| Guatemala | Guatemalan Quetzal | `GTQ` |
| Caribbean (most) | East Caribbean Dollar | `XCD` |
| Jamaica | Jamaican Dollar | `JMD` |
| Dominican Republic | Dominican Peso | `DOP` |
| Trinidad & Tobago | Trinidad Dollar | `TTD` |

---

## Implementation Status

### ✅ Completed (100% Ready)

- Project structure with Poetry, Docker
- Database models (shared with europe-scraper)
- Configuration for all 23 countries, 50+ lotteries
- Base scraper classes (Selenium, BS4)
- APScheduler integration with CRON
- FastAPI REST API (12 endpoints)
- Main entry point with startup sequence

### ✅ Working Scrapers (6 Implemented)

- 🇺🇸 USA: Powerball, Mega Millions
- 🇨🇦 Canada: Lotto 6/49, Lotto Max
- 🇲🇽 Mexico: Melate, Chispazo

### 🚧 Remaining Work (40+ Scrapers)

**Caribbean Countries:**
- Jamaica: Supreme Ventures Lotto, Cash Pot
- Dominican Republic: Leidsa Quiniela, Loteka
- Trinidad & Tobago: Play Whe, Lotto Plus
- Other Caribbean nations (13 more)

**Central America:**
- Guatemala, Costa Rica, Panama (national lotteries)
- Belize, Honduras, El Salvador, Nicaragua

**Estimated Effort:** 1-2 hours per scraper × 40 scrapers = 40-80 hours

---

## Integration with Platform

### Unified Database

The North America scraper **shares** the same database as:
- Next.js application (frontend + API)
- Europe scraper (21 lotteries)
- Asia scraper (13 lotteries)

**Benefits:**
- ✅ Single source of truth for all lottery data
- ✅ Cross-region queries (compare US and European jackpots)
- ✅ Unified API for frontend
- ✅ Consistent data format across all regions

### Region Differentiation

```sql
-- Query North American lotteries only
SELECT * FROM lottery WHERE region = 'North America';

-- Query all lotteries worldwide
SELECT region, COUNT(*) FROM lottery GROUP BY region;

-- Expected:
-- North America | 50+
-- Europe        | 21
-- Asia          | 13
```

---

## Deployment

### Local Development

```bash
cd services/northamerica-scraper

# Install dependencies
poetry install

# Configure environment
cp .env.example .env

# Initialize database
poetry run python -m src.database.populate_lotteries

# Run service
poetry run python -m src.main
```

### Docker Deployment

```bash
cd services/northamerica-scraper

# Build and start
docker-compose up --build -d

# Check logs
docker-compose logs -f scraper

# Health check
curl http://localhost:8002/health
```

---

## Monitoring

### Check Lottery Population

```sql
SELECT COUNT(*) FROM lottery WHERE region = 'North America';
-- Expected: 50+
```

### Check Recent Results

```sql
SELECT 
    l.name,
    r."drawDate",
    r.numbers,
    r.jackpot
FROM result r
JOIN lottery l ON r."lotteryId" = l.id
WHERE l.region = 'North America'
ORDER BY r."drawDate" DESC
LIMIT 10;
```

### Check Scraper Success Rate

```sql
SELECT 
    l.country,
    j.status,
    COUNT(*) as count
FROM scraper_job j
JOIN lottery l ON j."lotteryId" = l.id
WHERE l.region = 'North America'
  AND j."createdAt" > NOW() - INTERVAL '24 hours'
GROUP BY l.country, j.status;
```

---

## Resources

- 📖 **[Integration Guide](./northamerica-scraper-integration.md)** - Detailed database integration
- ⚡ **[Quick Start](./northamerica-scraper-quickstart.md)** - Get started in 5 minutes
- 🏗️ **[Full README](../services/northamerica-scraper/README.md)** - Complete technical documentation
- 🌍 **[Europe Scraper](./europe-scraper.md)** - Sister service for European lotteries
- 🌏 **[Asia Scraper](./asia-scraper.md)** - Sister service for Asian lotteries

---

## Support

For issues, questions, or contributions:
- Review the [Quick Start Guide](./northamerica-scraper-quickstart.md)
- Check the [Integration Guide](./northamerica-scraper-integration.md)
- Contact the development team

---

**Version:** 1.0.0  
**Status:** ✅ Foundation Complete | 🚧 Scrapers In Progress  
**Coverage:** 23 countries, 50+ lotteries configured, 6 scrapers implemented
