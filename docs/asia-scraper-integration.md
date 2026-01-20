# Asia Scraper - Database Integration Guide

## Overview

The **Asia Lottery Scraper** integrates seamlessly with the existing Next.js/Drizzle database schema, sharing the same PostgreSQL database with both the **Europe Scraper**, **North America Scraper**, and the **Next.js application**. This creates a unified data source for all lottery results across all global regions.

## Integration Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   PostgreSQL Database                     │
│                      (Port 5432)                          │
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
- ✍️ **Asia Scraper**: Writes 13+ Asian lotteries via `populate_lotteries.py`
- ✍️ **Europe Scraper**: Writes 21 European lotteries via `populate_lotteries.py`
- ✍️ **North America Scraper**: Writes 50+ North American lotteries via `populate_lotteries.py`
- ✍️ **Manual**: Admin could add other lotteries

**Who Reads:**
- 👁️ **Next.js API**: Queries all lotteries for frontend display
- 👁️ **Asia Scraper**: Looks up lottery IDs for result insertion
- 👁️ **Europe Scraper**: Looks up lottery IDs for result insertion
- 👁️ **North America Scraper**: Looks up lottery IDs for result insertion

#### 2. `result` Table

**Schema:**
```sql
CREATE TABLE result (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    "lotteryId" UUID REFERENCES lottery(id) NOT NULL,
    "drawDate" TIMESTAMP NOT NULL,
    numbers JSONB NOT NULL,          -- {"main": [1,2,3], "bonus": [4]}
    jackpot TEXT,                    -- "₹1Cr", "S$1M", "€50M", "$100M"
    currency TEXT,                   -- "INR", "SGD", "EUR", "USD"
    winners JSONB,                   -- [{"tier": 1, "prize": 1000000, "count": 1}]
    "createdAt" TIMESTAMP DEFAULT now(),
    UNIQUE("lotteryId", "drawDate")  -- Prevent duplicate results
);
```

**Who Writes:**
- ✍️ **Asia Scraper**: Writes Asian lottery results
- ✍️ **Europe Scraper**: Writes European lottery results
- ✍️ **North America Scraper**: Writes North American lottery results

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

**Purpose**: Track scraper execution history for Asia, Europe, and North America scrapers.

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

**Asian Examples:**

```python
# Singapore TOTO
{"main": [3, 12, 18, 24, 36, 42], "bonus": [15]}

# India Kerala Lottery
{"main": [1, 2, 3, 4, 5, 6]}

# Malaysia Magnum 4D
{"main": [1, 2, 3, 4]}

# Hong Kong Mark Six
{"main": [5, 12, 18, 24, 36, 42], "bonus": [7]}

# South Korea Lotto 6/45
{"main": [3, 12, 18, 24, 36, 42], "bonus": [15]}
```

### Jackpot Storage

Store as **formatted text string** with currency symbol:

```python
# ✅ CORRECT
jackpot = "₹1Cr"
currency = "INR"

jackpot = "S$2,500,000"
currency = "SGD"

jackpot = "RM 5M"
currency = "MYR"

# ❌ INCORRECT
jackpot = 10000000  # Don't store as number
```

**Why?** Formatted strings preserve the original display format and handle large numbers better.

### Currency Codes

Use **ISO 4217** currency codes:

| Country | Currency | Code |
|---------|----------|------|
| India | Indian Rupee | `INR` |
| Singapore | Singapore Dollar | `SGD` |
| Malaysia | Malaysian Ringgit | `MYR` |
| Thailand | Thai Baht | `THB` |
| Philippines | Philippine Peso | `PHP` |
| Japan | Japanese Yen | `JPY` |
| South Korea | South Korean Won | `KRW` |
| Taiwan | New Taiwan Dollar | `TWD` |
| Hong Kong | Hong Kong Dollar | `HKD` |
| Vietnam | Vietnamese Dong | `VND` |
| China | Chinese Yuan | `CNY` |
| Indonesia | Indonesian Rupiah | `IDR` |

## Integration Steps

### Step 1: Ensure Database Exists

The Asia scraper uses the **same database** as Europe scraper, North America scraper, and Next.js:

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

### Step 3: Initialize Asia Scraper Tables

```bash
cd /Users/kvivek/Documents/global_lottery_platform/services/asia-scraper

# Create scraper_job and scraper_config tables
# (lottery and result tables already exist from Next.js or other scrapers)
docker exec -it asia-lottery-scraper poetry run python -c "from src.database.session import init_db; init_db()"
```

**Note**: `init_db()` is idempotent - it won't recreate existing tables.

### Step 4: Populate Asian Lotteries

```bash
# Add 13+ Asian lotteries to shared lottery table
docker exec -it asia-lottery-scraper poetry run python src/database/populate_lotteries.py
```

**Expected Output:**
```
INFO: Added new lottery slug=sg-toto
INFO: Added new lottery slug=sg-4d
INFO: Added new lottery slug=in-kerala-lottery
INFO: Added new lottery slug=my-magnum-4d
...
INFO: Lottery population complete added=13 updated=0 total=13
```

### Step 5: Verify Integration

**Check via Next.js API:**
```bash
# Should show ALL lotteries (Asia, Europe, North America)
curl http://localhost:3000/api/lotteries | jq

# Expected: Singapore TOTO, Kerala Lottery, EuroMillions, Powerball, etc.
```

**Check via Asia Scraper API:**
```bash
curl http://localhost:8000/lotteries | jq
```

**Check via Database:**
```sql
SELECT region, COUNT(*) 
FROM lottery 
WHERE "isActive" = true
GROUP BY region;

-- Expected:
-- Asia          | 13
-- Europe        | 21
-- North America | 50+
```

## Data Flow

### 1. Initial Setup

```
Asia Scraper populate_lotteries.py
    ↓
Inserts 13+ Asian lotteries into `lottery` table
    ↓
Next.js API can now query Asian lotteries
```

### 2. Scheduled Scraping

```
APScheduler triggers (e.g., Mon 12:00 PM UTC for Singapore TOTO)
    ↓
Asia Scraper runs SingaporeTOTOScraper
    ↓
Scraper fetches latest results from website
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

### Test 1: Verify Asian Lotteries Appear in Next.js

```bash
# 1. Populate Asian lotteries
cd services/asia-scraper
docker exec -it asia-lottery-scraper poetry run python src/database/populate_lotteries.py

# 2. Query via Next.js API
curl http://localhost:3000/api/lotteries | jq '.[] | select(.country=="Singapore")'

# Expected output:
# {
#   "id": "...",
#   "slug": "sg-toto",
#   "name": "Singapore TOTO",
#   "country": "Singapore",
#   "region": "Asia"
# }
```

### Test 2: Scrape Asian Lottery and View in Next.js

```bash
# 1. Trigger scrape via Asia Scraper
curl -X POST http://localhost:8000/scrapers/sg-toto/run

# 2. Check results via Next.js API
curl http://localhost:3000/api/lotteries/sg-toto/results | jq

# Expected: Recent Singapore TOTO results with numbers, jackpot, drawDate
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
# Terminal 1: Asia Scraper
cd services/asia-scraper
docker-compose up

# Terminal 2: Europe Scraper
cd services/europe-scraper
docker-compose up

# Terminal 3: North America Scraper
cd services/northamerica-scraper
docker-compose up

# Terminal 4: Next.js App
cd apps/web
npm run dev
```

**Port Mapping:**
- Asia Scraper: `5432 (Postgres), 6379 (Redis), 8000 (API)`
- Europe Scraper: `5432 (Postgres), 6379 (Redis), 8001 (API)`
- North America Scraper: `5433 (Postgres), 6380 (Redis), 8002 (API)`
- Next.js: `3000 (Web)`

### Database Connection

All services connect to **one** PostgreSQL instance:
- Internal address: `postgres:5432` (inside Docker network)
- External address: `localhost:5432` (from host machine or different Docker networks)

## Troubleshooting Integration

### Issue: Asian lotteries not showing in Next.js

**Diagnosis:**
```sql
SELECT * FROM lottery WHERE region = 'Asia';
```

**Solution:**
```bash
# Re-run population script
cd services/asia-scraper
docker exec -it asia-lottery-scraper poetry run python src/database/populate_lotteries.py
```

### Issue: Results saving but not appearing in Next.js

**Check 1: Lottery is active**
```sql
SELECT slug, "isActive" FROM lottery WHERE slug = 'sg-toto';
```

**Check 2: Results exist**
```sql
SELECT * FROM result 
WHERE "lotteryId" IN (SELECT id FROM lottery WHERE slug = 'sg-toto')
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

**Explanation:** The Asia scraper tried to insert a result that already exists.

**Solution:** This is **expected behavior**. The deduplication logic prevents this, but you might see it in logs. The scraper will skip duplicates automatically.

### Issue: UUID format errors

**Error:**
```
DataError: invalid input syntax for type uuid: "123"
```

**Solution:** Ensure you're using UUID primary keys, not integers:
```python
from sqlalchemy.dialects.postgresql import UUID
import uuid

id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
```

## Benefits of Unified Integration

✅ **Single Source of Truth**: One `lottery` table for all lotteries worldwide  
✅ **Automatic Updates**: Asia scraper writes → Next.js shows immediately  
✅ **No Data Duplication**: Shared schema prevents inconsistencies  
✅ **Unified API**: Frontend queries one consistent API for all regions  
✅ **Easy Expansion**: Adding new regions (Africa, South America) follows same pattern  
✅ **Cross-Region Queries**: Compare Asian vs European vs North American jackpots easily  

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

### Monitor Asia Specific

```sql
-- Recent Asian results
SELECT 
    l.name,
    l.country,
    r."drawDate",
    r.jackpot,
    r.currency
FROM result r
JOIN lottery l ON r."lotteryId" = l.id
WHERE l.region = 'Asia'
ORDER BY r."drawDate" DESC
LIMIT 20;

-- Asia scraper performance
SELECT 
    l.name,
    COUNT(j.id) as total_jobs,
    SUM(CASE WHEN j.status = 'success' THEN 1 ELSE 0 END) as success_count,
    SUM(CASE WHEN j.status = 'failed' THEN 1 ELSE 0 END) as failed_count,
    AVG(j."executionTimeMs") as avg_time_ms
FROM scraper_job j
JOIN lottery l ON j."lotteryId" = l.id
WHERE l.region = 'Asia'
  AND j."createdAt" > NOW() - INTERVAL '7 days'
GROUP BY l.name
ORDER BY total_jobs DESC;
```

## Next Steps

1. ✅ Run integration tests ([asia-scraper-quickstart.md](./asia-scraper-quickstart.md))
2. ✅ Verify data appears in Next.js frontend
3. ✅ Monitor scraper job success rates
4. ✅ Set up production database with proper backups
5. ✅ Deploy all three scrapers together (Asia, Europe, North America)
6. ✅ Configure CRON schedules for production

## API Integration Examples

### Next.js API Route Example

```typescript
// app/api/lotteries/route.ts
import { db } from "@/lib/db";
import { lottery, result } from "@/lib/db/schema";

export async function GET() {
  // This query works for ALL lotteries (Asia, Europe, North America, etc.)
  const lotteries = await db
    .select()
    .from(lottery)
    .where(eq(lottery.isActive, true))
    .orderBy(lottery.region, lottery.country, lottery.name);
  
  return Response.json(lotteries);
}

// app/api/lotteries/asia/route.ts
export async function GET() {
  // Get only Asian lotteries
  const asianLotteries = await db
    .select()
    .from(lottery)
    .where(
      and(
        eq(lottery.isActive, true),
        eq(lottery.region, 'Asia')
      )
    )
    .orderBy(lottery.country, lottery.name);
  
  return Response.json(asianLotteries);
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
      {region === "Asia" && <h2>Asian Lotteries</h2>}
      {region === "Europe" && <h2>European Lotteries</h2>}
      {region === "North America" && <h2>North American Lotteries</h2>}
      
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

The Asia Lottery Scraper integrates seamlessly with the existing database infrastructure:

- 📊 **Shares** `lottery` and `result` tables with Europe scraper, North America scraper, and Next.js
- 🔧 **Adds** `scraper_job` and `scraper_config` tables for internal tracking
- 🌏 **Contributes** 13+ lottery configurations to the shared ecosystem
- 🔄 **Maintains** data consistency through JSONB standards and UUID primary keys
- ✅ **Enables** cross-region queries and unified frontend display
- 🔌 **Coexists** with other scrapers using different ports but same database

For detailed deployment instructions, see [asia-scraper-quickstart.md](./asia-scraper-quickstart.md).
