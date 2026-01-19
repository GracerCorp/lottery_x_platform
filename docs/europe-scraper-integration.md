# Europe Scraper - Database Integration Guide

## Overview

The **Europe Lottery Scraper** integrates seamlessly with the existing Next.js/Drizzle database schema, sharing the same PostgreSQL database with both the **Asia Scraper** and the **Next.js application**. This creates a unified data source for all lottery results across all regions.

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
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────┴────┐      ┌─────┴────┐      ┌────┴────┐
    │ Next.js │      │  Asia    │      │ Europe  │
    │   App   │      │ Scraper  │      │ Scraper │
    │ :3000   │      │  :8000   │      │  :8001  │
    └─────────┘      └──────────┘      └─────────┘
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
- ✍️ **Europe Scraper**: Writes 21 European lotteries via `populate_lotteries.py`
- ✍️ **Asia Scraper**: Writes 13 Asian lotteries via `populate_lotteries.py`
- ✍️ **Manual**: Admin could add US/other lotteries

**Who Reads:**
- 👁️ **Next.js API**: Queries all lotteries for frontend display
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
    jackpot TEXT,                    -- "€100M", "₹50Cr", "$1.5M"
    currency TEXT,                   -- "EUR", "USD", "INR", "GBP"
    winners JSONB,                   -- [{"tier": 1, "prize": 1000000, "count": 1}]
    "createdAt" TIMESTAMP DEFAULT now(),
    UNIQUE("lotteryId", "drawDate")  -- Prevent duplicate results
);
```

**Who Writes:**
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

**Purpose**: Track scraper execution history for both Europe and Asia scrapers.

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
    "extra": [8]                      # Optional: Extra numbers (e.g., Lucky Stars)
}

# ❌ INCORRECT (Old format)
winning_numbers = [1, 2, 3, 4, 5, 6]  # Don't use separate arrays
bonus_numbers = [7]
```

**European Examples:**

```python
# UK National Lottery
{"main": [3, 15, 23, 31, 42, 59], "bonus": [12]}

# EuroMillions
{"main": [7, 14, 21, 28, 35], "bonus": [3, 9]}  # Lucky Stars

# Spain La Primitiva
{"main": [5, 12, 18, 24, 36, 42], "complement": [15], "reintegro": [3]}
```

### Jackpot Storage

Store as **formatted text string** with currency symbol:

```python
# ✅ CORRECT
jackpot = "€100M"
currency = "EUR"

jackpot = "£5,000,000"
currency = "GBP"

jackpot = "CHF 25M"
currency = "CHF"

# ❌ INCORRECT
jackpot = 100000000  # Don't store as number
```

**Why?** Formatted strings preserve the original display format and handle large numbers better.

### Currency Codes

Use **ISO 4217** currency codes:

| Region | Currency | Code |
|--------|----------|------|
| Europe (most) | Euro | `EUR` |
| UK | British Pound | `GBP` |
| Switzerland | Swiss Franc | `CHF` |
| Poland | Polish Złoty | `PLN` |
| Sweden | Swedish Krona | `SEK` |
| Norway | Norwegian Krone | `NOK` |
| Denmark | Danish Krone | `DKK` |
| Czech Republic | Czech Koruna | `CZK` |
| Hungary | Hungarian Forint | `HUF` |

## Integration Steps

### Step 1: Ensure Database Exists

The Europe scraper uses the **same database** as Asia scraper and Next.js:

```bash
# Check if database exists
psql -l | grep lottery_db

# If not, create it (Docker will do this automatically)
createdb lottery_db
```

### Step 2: Both Scrapers Use Same DATABASE_URL

**Asia Scraper `.env`:**
```bash
DATABASE_URL=postgresql://lottery_user:lottery_pass@postgres:5432/lottery_db
```

**Europe Scraper `.env`:**
```bash
DATABASE_URL=postgresql://lottery_user:lottery_pass@postgres:5432/lottery_db
```

**Next.js `.env.local`:**
```bash
DATABASE_URL=postgresql://lottery_user:lottery_pass@localhost:5432/lottery_db
```

### Step 3: Initialize Europe Scraper Tables

```bash
cd /Users/kvivek/Documents/global_lottery_platform/services/europe-scraper

# Create scraper_job and scraper_config tables
# (lottery and result tables already exist from Next.js or Asia scraper)
docker exec -it europe-lottery-scraper poetry run python -c "from src.database.session import init_db; init_db()"
```

**Note**: `init_db()` is idempotent - it won't recreate existing tables.

### Step 4: Populate European Lotteries

```bash
# Add 21 European lotteries to shared lottery table
docker exec -it europe-lottery-scraper poetry run python src/database/populate_lotteries.py
```

**Expected Output:**
```
INFO: Added new lottery slug=uk-national-lottery
INFO: Added new lottery slug=fr-loto
INFO: Added new lottery slug=es-primitiva
...
INFO: Lottery population complete added=21 updated=0 total=21
```

### Step 5: Verify Integration

**Check via Next.js API:**
```bash
# Should show ALL lotteries (US, Europe, Asia)
curl http://localhost:3000/api/lotteries | jq

# Expected: Powerball, EuroMillions, Singapore TOTO, UK Lotto, etc.
```

**Check via Europe Scraper API:**
```bash
curl http://localhost:8001/lotteries | jq
```

**Check via Database:**
```sql
SELECT region, COUNT(*) 
FROM lottery 
WHERE "isActive" = true
GROUP BY region;

-- Expected:
-- Europe      | 21
-- Asia        | 13
-- North America | X (if you have US lotteries)
```

## Data Flow

### 1. Initial Setup

```
Europe Scraper populate_lotteries.py
    ↓
Inserts 21 European lotteries into `lottery` table
    ↓
Next.js API can now query European lotteries
```

### 2. Scheduled Scraping

```
APScheduler triggers (e.g., Wed 9 PM UTC for UK Lotto)
    ↓
Europe Scraper runs UKNationalLotteryScraper
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

### Test 1: Verify European Lotteries Appear in Next.js

```bash
# 1. Populate European lotteries
cd services/europe-scraper
docker exec -it europe-lottery-scraper poetry run python src/database/populate_lotteries.py

# 2. Query via Next.js API
curl http://localhost:3000/api/lotteries | jq '.[] | select(.country=="United Kingdom")'

# Expected output:
# {
#   "id": "...",
#   "slug": "uk-national-lottery",
#   "name": "UK National Lottery",
#   "country": "United Kingdom",
#   "region": "Europe"
# }
```

### Test 2: Scrape European Lottery and View in Next.js

```bash
# 1. Trigger scrape via Europe Scraper
curl -X POST http://localhost:8001/scrapers/uk-national-lottery/run

# 2. Check results via Next.js API
curl http://localhost:3000/api/lotteries/uk-national-lottery/results | jq

# Expected: Recent UK Lotto results with numbers, jackpot, drawDate
```

### Test 3: Verify Both Asia and Europe Results Coexist

```sql
-- Connect to database
psql $DATABASE_URL

-- Query results from both regions
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
-- Asia      | Singapore   | TOTO                  | 5
-- Asia      | India       | Kerala State Lottery  | 10
-- Europe    | UK          | National Lottery      | 3
-- Europe    | Spain       | La Primitiva          | 8
```

## Migration from Separate Databases (If Applicable)

If you previously had Europe and Asia scrapers using **separate databases**, follow this migration:

### Step 1: Backup All Data

```bash
# Backup Asia scraper database
pg_dump asia_lottery_db > asia_backup.sql

# Backup Europe scraper database (if exists)
pg_dump europe_lottery_db > europe_backup.sql
```

### Step 2: Create Unified Database

```bash
# Create new unified database
createdb lottery_db

# Run Next.js migrations (creates base schema)
cd apps/web
npx drizzle-kit push:pg
```

### Step 3: Migrate Asia Data

```bash
# Re-populate Asia lotteries
cd services/asia-scraper
poetry run python src/database/populate_lotteries.py

# Optionally import old results
psql lottery_db < asia_results_only.sql
```

### Step 4: Migrate Europe Data

```bash
# Populate Europe lotteries
cd services/europe-scraper
poetry run python src/database/populate_lotteries.py

# Optionally import old results
psql lottery_db < europe_results_only.sql
```

### Step 5: Update Connection Strings

Update `.env` in all services to use `lottery_db`.

## Troubleshooting Integration

### Issue: European lotteries not showing in Next.js

**Diagnosis:**
```sql
SELECT * FROM lottery WHERE region = 'Europe';
```

**Solution:**
```bash
# Re-run population script
cd services/europe-scraper
docker exec -it europe-lottery-scraper poetry run python src/database/populate_lotteries.py
```

### Issue: Results saving but not appearing in Next.js

**Check 1: Lottery is active**
```sql
SELECT slug, "isActive" FROM lottery WHERE slug = 'uk-national-lottery';
```

**Check 2: Results exist**
```sql
SELECT * FROM result 
WHERE "lotteryId" IN (SELECT id FROM lottery WHERE slug = 'uk-national-lottery')
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

**Explanation:** The Europe scraper tried to insert a result that already exists.

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
✅ **Automatic Updates**: Europe scraper writes → Next.js shows immediately
✅ **No Data Duplication**: Shared schema prevents inconsistencies
✅ **Unified API**: Frontend queries one consistent API for all regions
✅ **Easy Expansion**: Adding new regions (Africa, South America) follows same pattern
✅ **Cross-Region Queries**: Compare results across continents easily

## Monitoring Integration

### Check Total Lottery Count

```sql
SELECT region, COUNT(*) as lottery_count
FROM lottery
WHERE "isActive" = true
GROUP BY region
ORDER BY lottery_count DESC;

-- Expected:
-- Europe      | 21
-- Asia        | 13
-- ...
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

## Next Steps

1. ✅ Run integration tests ([europe-scraper-quickstart.md](./europe-scraper-quickstart.md))
2. ✅ Verify data appears in Next.js frontend
3. ✅ Monitor scraper job success rates
4. ✅ Set up production database with proper backups
5. ✅ Deploy both Europe and Asia scrapers together
6. ✅ Configure CRON schedules for production

## API Integration Examples

### Next.js API Route Example

```typescript
// app/api/lotteries/route.ts
import { db } from "@/lib/db";
import { lottery, result } from "@/lib/db/schema";

export async function GET() {
  // This query works for ALL lotteries (Asia, Europe, US, etc.)
  const lotteries = await db
    .select()
    .from(lottery)
    .where(eq(lottery.isActive, true))
    .orderBy(lottery.country, lottery.name);
  
  return Response.json(lotteries);
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
      {region === "Europe" && <h2>European Lotteries</h2>}
      {region === "Asia" && <h2>Asian Lotteries</h2>}
      
      {lotteries?.map((lottery) => (
        <LotteryCard key={lottery.id} lottery={lottery} />
      ))}
    </div>
  )
}
```

## Summary

The Europe Lottery Scraper integrates seamlessly with the existing database infrastructure:

- 📊 **Shares** `lottery` and `result` tables with Asia scraper and Next.js
- 🔧 **Adds** `scraper_job` and `scraper_config` tables for internal tracking
- 🌍 **Contributes** 21 lottery configurations to the shared ecosystem
- 🔄 **Maintains** data consistency through JSONB standards and UUID primary keys
- ✅ **Enables** cross-region queries and unified frontend display

For detailed deployment instructions, see [europe-scraper-quickstart.md](./europe-scraper-quickstart.md).
