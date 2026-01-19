# North America Scraper - Database Integration Guide

## Overview

The **North America Lottery Scraper** integrates seamlessly with the existing Next.js/Drizzle database schema, sharing the same PostgreSQL database with both the **Europe Scraper**, **Asia Scraper**, and the **Next.js application**. This creates a unified data source for all lottery results across all global regions.

## Integration Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   PostgreSQL Database                     │
│                      (Port 5432/5433)                     │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │              Shared Tables                          │ │
│  │  ┌─────────┐  ┌────────┐                           │ │
│  │  │ lottery │  │ result │                           │ │
│  │  └────┬────┘  └───┬────┘                           │ │
│  │       │           │                                 │ │
│  └───────┼───────────┼─────────────────────────────────┘ │
│          │           │                                   │
│  ┌───────┼───────────┼─────────────────────────────────┐ │
│  │ Service-Specific Tables                             │ │
│  │  ┌─────────────┐  ┌────────────────┐               │ │
│  │  │ scraper_job │  │ scraper_config │  (Python)     │ │
│  │  └─────────────┘  └────────────────┘               │ │
│  │  ┌──────┐  ┌─────────┐  ┌──────────────┐           │ │
│  │  │ user │  │ session │  │ subscription │ (Next.js) │ │
│  │  └──────┘  └─────────┘  └──────────────┘           │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
                           ▲
         ┌─────────────────┼─────────────────┬────────────┐
         │                 │                 │            │
    ┌────┴────┐      ┌─────┴────┐      ┌────┴────┐  ┌───┴────┐
    │ Next.js │      │  Asia    │      │ Europe  │  │  North │
    │   App   │      │ Scraper  │      │ Scraper │  │ America│
    │ :3000   │      │  :8000   │      │  :8001  │  │ :8002  │
    └─────────┘      └──────────┘      └─────────┘  └────────┘
```

## Database Schema Compatibility

### Shared Tables (Used by All Services)

#### 1. `lottery` Table

**Schema:**
```sql
CREATE TABLE lottery (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    country TEXT NOT NULL,
    region TEXT,                   -- 'Asia', 'Europe', 'North America'
    frequency TEXT,
    logo TEXT,
    description TEXT,
    "officialLink" TEXT,
    "isActive" BOOLEAN DEFAULT true,
    "createdAt" TIMESTAMP DEFAULT now(),
    "updatedAt" TIMESTAMP DEFAULT now()
);
```

**Who Writes:**
- ✍️ **North America Scraper**: Writes 50+ North American lotteries via `populate_lotteries.py`
- ✍️ **Europe Scraper**: Writes 21 European lotteries via `populate_lotteries.py`
- ✍️ **Asia Scraper**: Writes 13 Asian lotteries via `populate_lotteries.py`
- ✍️ **Manual**: Admin could add other lotteries

**Who Reads:**
- 👁️ **Next.js API**: Queries all lotteries for frontend display
- 👁️ **North America Scraper**: Looks up lottery IDs for result insertion
- 👁️ **Europe Scraper**: Looks up lottery IDs for result insertion
- 👁️ **Asia Scraper**: Looks up lottery IDs for result insertion

#### 2. `result` Table

**Schema:**
```sql
CREATE TABLE result (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "lotteryId" UUID REFERENCES lottery(id) NOT NULL,
    "drawDate" TIMESTAMP NOT NULL,
    numbers JSONB NOT NULL,          -- {"main": [1,2,3], "bonus": [4]}
    jackpot TEXT,                    -- "$100M", "€50M", "₹1Cr"
    currency TEXT,                   -- "USD", "CAD", "MXN", "EUR", "INR"
    winners JSONB,                   -- [{"tier": 1, "prize": 1000000, "count": 1}]
    "createdAt" TIMESTAMP DEFAULT now(),
    UNIQUE("lotteryId", "drawDate")  -- Prevent duplicate results
);
```

**Who Writes:**
- ✍️ **North America Scraper**: Writes North American lottery results
- ✍️ **Europe Scraper**: Writes European lottery results
- ✍️ **Asia Scraper**: Writes Asian lottery results

**Who Reads:**
- 👁️ **Next.js API**: Reads all results for frontend display
- 👁️ **Frontend**: Displays results to users

### Service-Specific Tables

#### 3. `scraper_job` Table (Python Only)

```sql
CREATE TABLE scraper_job (
    id SERIAL PRIMARY KEY,
    "lotteryId" UUID REFERENCES lottery(id),
    status VARCHAR(20) NOT NULL,     -- 'pending', 'running', 'success', 'failed'
    "startedAt" TIMESTAMP,
    "completedAt" TIMESTAMP,
    "errorMessage" TEXT,
    "resultsCount" INTEGER DEFAULT 0,
    "executionTimeMs" INTEGER,
    "createdAt" TIMESTAMP DEFAULT now()
);
```

**Purpose**: Track scraper execution history for North America, Europe, and Asia scrapers.

#### 4. `scraper_config` Table (Python Only)

```sql
CREATE TABLE scraper_config (
    id SERIAL PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value JSONB NOT NULL,
    description TEXT,
    "updatedAt" TIMESTAMP DEFAULT now()
);
```

**Purpose**: Store dynamic configuration (CRON schedules, feature flags, etc.)

## Data Format Standards

### Numbers Storage

All scrapers must use the **unified JSONB format**:

```python
# ✅ CORRECT (Shared format)
numbers = {
    "main": [1, 2, 3, 4, 5, 6],      # Main numbers (sorted)
    "bonus": [7],                     # Bonus/supplementary numbers
    "extra": [8]                      # Optional: Extra numbers
}

# ❌ INCORRECT (Old format)
winning_numbers = [1, 2, 3, 4, 5, 6]  # Don't use separate arrays
bonus_numbers = [7]
```

**North American Examples:**

```python
# US Powerball
{"main": [5, 15, 25, 35, 45], "bonus": [10]}

# US Mega Millions
{"main": [7, 14, 21, 28, 35], "bonus": [6]}

# Canada Lotto 6/49
{"main": [3, 12, 18, 24, 36, 42], "bonus": [15]}

# Canada Lotto Max
{"main": [1, 8, 15, 22, 29, 36, 43]}

# Mexico Melate
{"main": [5, 12, 18, 24, 36, 42], "bonus": [7]}
```

### Jackpot Storage

Store as **formatted text string** with currency symbol:

```python
# ✅ CORRECT
jackpot = "$100M"
currency = "USD"

jackpot = "C$25,000,000"
currency = "CAD"

jackpot = "$200 Million MXN"
currency = "MXN"

# ❌ INCORRECT
jackpot = 100000000  # Don't store as number
```

**Why?** Formatted strings preserve the original display format and handle large numbers better.

### Currency Codes

Use **ISO 4217** currency codes:

| Region | Currency | Code |
|--------|----------|------|
| United States | US Dollar | `USD` |
| Canada | Canadian Dollar | `CAD` |
| Mexico | Mexican Peso | `MXN` |
| Costa Rica | Costa Rican Colón | `CRC` |
| Panama | Panamanian Balboa | `PAB` |
| Guatemala | Guatemalan Quetzal | `GTQ` |
| Honduras | Honduran Lempira | `HNL` |
| Nicaragua | Nicaraguan Córdoba | `NIO` |
| Jamaica | Jamaican Dollar | `JMD` |
| Dominican Republic | Dominican Peso | `DOP` |
| Haiti | Haitian Gourde | `HTG` |
| Barbados | Barbadian Dollar | `BBD` |
| Caribbean (most) | East Caribbean Dollar | `XCD` |
| Trinidad & Tobago | Trinidad Dollar | `TTD` |

## Integration Steps

### Step 1: Ensure Database Exists

The North America scraper uses the **same database** as Asia scraper, Europe scraper, and Next.js:

```bash
# Check if database exists
psql -l | grep lottery_db

# If not, create it (Docker will do this automatically)
createdb lottery_db
```

### Step 2: All Scrapers Use Same DATABASE_URL

**Asia Scraper `.env`:**
```bash
DATABASE_URL=postgresql://lottery_user:lottery_pass@postgres:5432/lottery_db
```

**Europe Scraper `.env`:**
```bash
DATABASE_URL=postgresql://lottery_user:lottery_pass@postgres:5432/lottery_db
```

**North America Scraper `.env`:**
```bash
DATABASE_URL=postgresql://lottery_user:lottery_pass@postgres:5432/lottery_db
```

**Next.js `.env.local`:**
```bash
DATABASE_URL=postgresql://lottery_user:lottery_pass@localhost:5432/lottery_db
```

> **Note**: North America scraper Docker uses different external ports (5433, 6380, 8002) to avoid conflicts when running all services simultaneously, but internally all connect to the same shared database.

### Step 3: Initialize North America Scraper Tables

```bash
cd /Users/kvivek/Documents/global_lottery_platform/services/northamerica-scraper

# Create scraper_job and scraper_config tables
# (lottery and result tables already exist from Next.js or other scrapers)
docker exec -it northamerica-lottery-scraper poetry run python -c "from src.database.session import init_db; init_db()"
```

**Note**: `init_db()` is idempotent - it won't recreate existing tables.

### Step 4: Populate North American Lotteries

```bash
# Add 50+ North American lotteries to shared lottery table
docker exec -it northamerica-lottery-scraper poetry run python src/database/populate_lotteries.py
```

**Expected Output:**
```
INFO: Added new lottery slug=us-powerball
INFO: Added new lottery slug=us-megamillions
INFO: Added new lottery slug=ca-lotto649
INFO: Added new lottery slug=ca-lottomax
INFO: Added new lottery slug=mx-melate
...
INFO: Lottery population complete added=50 updated=0 total=50
```

### Step 5: Verify Integration

**Check via Next.js API:**
```bash
# Should show ALL lotteries (North America, Europe, Asia)
curl http://localhost:3000/api/lotteries | jq

# Expected: Powerball, Mega Millions, Lotto 6/49, EuroMillions, Singapore TOTO, etc.
```

**Check via North America Scraper API:**
```bash
curl http://localhost:8002/lotteries | jq
```

**Check via Database:**
```sql
SELECT region, COUNT(*) 
FROM lottery 
WHERE "isActive" = true
GROUP BY region;

-- Expected:
-- North America | 50+
-- Europe        | 21
-- Asia          | 13
```

## Data Flow

### 1. Initial Setup

```
North America Scraper populate_lotteries.py
    ↓
Inserts 50+ North American lotteries into `lottery` table
    ↓
Next.js API can now query North American lotteries
```

### 2. Scheduled Scraping

```
APScheduler triggers (e.g., Mon 3:59 AM UTC for Powerball)
    ↓
North America Scraper runs PowerballScraper
    ↓
Scraper fetches latest results from powerball.com
    ↓
Parser extracts numbers, jackpot, draw date
    ↓
Saves to `result` table with lotteryId reference
    ↓
Creates/updates `scraper_job` record
    ↓
Next.js API immediately sees new results
    ↓
Frontend displays to users
```

### 3. Deduplication

```
Before inserting result:
    ↓
Check if result exists: 
  SELECT * FROM result 
  WHERE "lotteryId" = ? AND "drawDate" = ?
    ↓
If exists → Skip (log as duplicate)
If new → Insert
```

## Testing Integration

### Test 1: Verify North American Lotteries Appear in Next.js

```bash
# 1. Populate North American lotteries
cd services/northamerica-scraper
docker exec -it northamerica-lottery-scraper poetry run python src/database/populate_lotteries.py

# 2. Query via Next.js API
curl http://localhost:3000/api/lotteries | jq '.[] | select(.country=="United States")'

# Expected output:
# {
#   "id": "...",
#   "slug": "us-powerball",
#   "name": "Powerball",
#   "country": "United States",
#   "region": "North America"
# }
```

### Test 2: Scrape North American Lottery and View in Next.js

```bash
# 1. Trigger scrape via North America Scraper
curl -X POST http://localhost:8002/scrapers/us-powerball/run

# 2. Check results via Next.js API
curl http://localhost:3000/api/lotteries/us-powerball/results | jq

# Expected: Recent Powerball results with numbers, jackpot, drawDate
```

### Test 3: Verify All Three Regions Coexist

```sql
-- Connect to database
psql $DATABASE_URL

-- Query results from all regions
SELECT 
    l.region,
    l.country,
    l.name,
    COUNT(r.id) as results_count
FROM lottery l
LEFT JOIN result r ON l.id = r."lotteryId"
WHERE l."isActive" = true
GROUP BY l.region, l.country, l.name
ORDER BY l.region, l.country;

-- Expected:
-- Asia          | Singapore   | TOTO                  | 5
-- Asia          | India       | Kerala State Lottery  | 10
-- Europe        | UK          | National Lottery      | 3
-- Europe        | Spain       | La Primitiva          | 8
-- North America | USA         | Powerball             | 5
-- North America | Canada      | Lotto 6/49            | 3
```

## Running All Scrapers Together

### Shared Database Architecture

All three scrapers can run simultaneously against the same database:

```bash
# Terminal 1: Europe Scraper
cd services/europe-scraper
docker-compose up

# Terminal 2: Asia Scraper
cd services/asia-scraper
docker-compose up

# Terminal 3: North America Scraper
cd services/northamerica-scraper
docker-compose up

# Terminal 4: Next.js App
cd apps/web
npm run dev
```

**Port Mapping:**
- Europe Scraper: `5432 (Postgres), 6379 (Redis), 8001 (API)`
- Asia Scraper: `5432 (Postgres), 6379 (Redis), 8000 (API)`
- North America Scraper: `5433 (Postgres), 6380 (Redis), 8002 (API)`
- Next.js: `3000 (Web)`

### Database Connection

All services connect to **one** PostgreSQL instance:
- Internal address: `postgres:5432` (inside Docker network)
- External address: `localhost:5432` (from host machine or different Docker networks)

## Troubleshooting Integration

### Issue: North American lotteries not showing in Next.js

**Diagnosis:**
```sql
SELECT * FROM lottery WHERE region = 'North America';
```

**Solution:**
```bash
# Re-run population script
cd services/northamerica-scraper
docker exec -it northamerica-lottery-scraper poetry run python src/database/populate_lotteries.py
```

### Issue: Results saving but not appearing in Next.js

**Check 1: Lottery is active**
```sql
SELECT slug, "isActive" FROM lottery WHERE slug = 'us-powerball';
```

**Check 2: Results exist**
```sql
SELECT * FROM result 
WHERE "lotteryId" IN (SELECT id FROM lottery WHERE slug = 'us-powerball')
ORDER BY "drawDate" DESC 
LIMIT 5;
```

**Check 3: Next.js cache**
```bash
# Clear Next.js cache
cd apps/web
rm -rf .next
npm run dev
```

### Issue: Duplicate key errors

**Error:**
```
IntegrityError: duplicate key value violates unique constraint "result_lotteryId_drawDate_key"
```

**Explanation:** The North America scraper tried to insert a result that already exists.

**Solution:** This is **expected behavior**. The deduplication logic prevents this, but you might see it in logs. The scraper will skip duplicates automatically.

### Issue: Port conflicts between scrapers

**Error:**
```
Error: Port 5432 is already in use
```

**Solution:** North America scraper uses different ports:
```yaml
# docker-compose.yml
postgres:
  ports:
    - "5433:5432"  # External:Internal
redis:
  ports:
    - "6380:6379"
scraper:
  ports:
    - "8002:8002"
```

But internally, all connect to the **shared** database via Docker network.

## Benefits of Unified Integration

✅ **Single Source of Truth**: One `lottery` table for all lotteries worldwide  
✅ **Automatic Updates**: North America scraper writes → Next.js shows immediately  
✅ **No Data Duplication**: Shared schema prevents inconsistencies  
✅ **Unified API**: Frontend queries one consistent API for all regions  
✅ **Easy Expansion**: Adding new regions (South America, Africa) follows same pattern  
✅ **Cross-Region Queries**: Compare Powerball vs EuroMillions jackpots easily  

## Monitoring Integration

### Check Total Lottery Count

```sql
SELECT region, COUNT(*) as lottery_count
FROM lottery
WHERE "isActive" = true
GROUP BY region
ORDER BY lottery_count DESC;

-- Expected:
-- North America | 50+
-- Europe        | 21
-- Asia          | 13
```

### Check Results by Region

```sql
SELECT 
    l.region,
    COUNT(DISTINCT l.id) as lottery_count,
    COUNT(r.id) as total_results,
    MAX(r."createdAt") as last_result_time
FROM lottery l
LEFT JOIN result r ON l.id = r."lotteryId"
WHERE l."isActive" = true
GROUP BY l.region;
```

### Check Scraper Job Success Rate

```sql
SELECT 
    l.region,
    l.country,
    j.status,
    COUNT(*) as job_count
FROM scraper_job j
JOIN lottery l ON j."lotteryId" = l.id
WHERE j."createdAt" > NOW() - INTERVAL '24 hours'
GROUP BY l.region, l.country, j.status
ORDER BY l.region, l.country, j.status;
```

### Monitor North America Specific

```sql
-- Recent North American results
SELECT 
    l.name,
    l.country,
    r."drawDate",
    r.jackpot,
    r.currency
FROM result r
JOIN lottery l ON r."lotteryId" = l.id
WHERE l.region = 'North America'
ORDER BY r."drawDate" DESC
LIMIT 20;

-- North America scraper performance
SELECT 
    l.name,
    COUNT(j.id) as total_jobs,
    SUM(CASE WHEN j.status = 'success' THEN 1 ELSE 0 END) as success_count,
    SUM(CASE WHEN j.status = 'failed' THEN 1 ELSE 0 END) as failed_count,
    AVG(j."executionTimeMs") as avg_time_ms
FROM scraper_job j
JOIN lottery l ON j."lotteryId" = l.id
WHERE l.region = 'North America'
  AND j."createdAt" > NOW() - INTERVAL '7 days'
GROUP BY l.name
ORDER BY total_jobs DESC;
```

## Next Steps

1. ✅ Run integration tests ([northamerica-scraper-quickstart.md](./northamerica-scraper-quickstart.md))
2. ✅ Verify data appears in Next.js frontend
3. ✅ Monitor scraper job success rates
4. ✅ Set up production database with proper backups
5. ✅ Deploy all three scrapers together (North America, Europe, Asia)
6. ✅ Configure CRON schedules for production

## API Integration Examples

### Next.js API Route Example

```typescript
// app/api/lotteries/route.ts
import { db } from "@/lib/db";
import { lottery, result } from "@/lib/db/schema";

export async function GET() {
  // This query works for ALL lotteries (North America, Europe, Asia, etc.)
  const lotteries = await db
    .select()
    .from(lottery)
    .where(eq(lottery.isActive, true))
    .orderBy(lottery.region, lottery.country, lottery.name);
  
  return Response.json(lotteries);
}

// app/api/lotteries/north-america/route.ts
export async function GET() {
  // Get only North American lotteries
  const northAmericaLotteries = await db
    .select()
    .from(lottery)
    .where(
      and(
        eq(lottery.isActive, true),
        eq(lottery.region, 'North America')
      )
    )
    .orderBy(lottery.country, lottery.name);
  
  return Response.json(northAmericaLotteries);
}
```

### Frontend Component Example

```typescript
// components/lottery-results.tsx
"use client"

export function LotteryResults({ region }: { region: string }) {
  const { data: lotteries } = useSWR(`/api/lotteries?region=${region}`)
  
  return (
    <div>
      {region === "North America" && <h2>North American Lotteries</h2>}
      {region === "Europe" && <h2>European Lotteries</h2>}
      {region === "Asia" && <h2>Asian Lotteries</h2>}
      
      {lotteries?.map((lottery) => (
        <LotteryCard key={lottery.id} lottery={lottery} />
      ))}
    </div>
  )
}

// components/global-jackpots.tsx
export function GlobalJackpots() {
  // Compare jackpots across all regions
  const { data } = useSWR('/api/lotteries/top-jackpots')
  
  return (
    <div>
      <h2>Biggest Jackpots Worldwide</h2>
      {data?.map(lottery => (
        <div key={lottery.id}>
          <span>{lottery.name}</span>
          <span>{lottery.country}</span>
          <span className="jackpot">{lottery.latestJackpot}</span>
        </div>
      ))}
    </div>
  )
}
```

## Summary

The North America Lottery Scraper integrates seamlessly with the existing database infrastructure:

- 📊 **Shares** `lottery` and `result` tables with Europe scraper, Asia scraper, and Next.js
- 🔧 **Adds** `scraper_job` and `scraper_config` tables for internal tracking
- 🌎 **Contributes** 50+ lottery configurations to the shared ecosystem
- 🔄 **Maintains** data consistency through JSONB standards and UUID primary keys
- ✅ **Enables** cross-region queries and unified frontend display
- 🔌 **Coexists** with other scrapers using different ports but same database

For detailed deployment instructions, see [northamerica-scraper-quickstart.md](./northamerica-scraper-quickstart.md).
