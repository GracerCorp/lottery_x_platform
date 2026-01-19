# Database Integration - Migration Guide

## Overview

The Python Asia scraper has been integrated with the existing Next.js/Drizzle database schema.

## What Changed

### Database Schema

**Before:**
- Separate tables: `lotteries`, `lottery_results`, `countries`
- Integer primary keys
- Python-only schema

**After:**
- Shared tables: `lottery`, `result`
- UUID primary keys (matching Next.js schema)
- New scraper tables: `scraper_job`, `scraper_config`

### Data Format

**Numbers Storage:**
```python
# Before (Python only)
winning_numbers = [1, 2, 3, 4, 5, 6]  # ARRAY
bonus_numbers = [7]  # ARRAY

# After (Shared format)
numbers = {
    "main": [1, 2, 3, 4, 5, 6],
    "bonus": [7]
}  # JSONB
```

**Jackpot Storage:**
```python
# Before
jackpot_amount = 1000000.00  # Numeric
currency = "USD"

# After
jackpot = "$1.0M"  # Text with formatted amount
currency = "USD"
```

## Migration Steps

### 1. Update Database Connection

Both systems use the same DATABASE_URL:

```bash
# .env (Python scraper)
DATABASE_URL=postgresql://user:pass@localhost:5432/lottery_platform

# .env.local (Next.js)
DATABASE_URL=postgresql://user:pass@localhost:5432/lottery_platform
```

### 2. Create New Python Tables

```bash
cd services/asia-scraper

# Initialize database (creates scraper_job and scraper_config tables)
poetry run python -c "from src.database.session import init_db; init_db()"
```

### 3. Populate Asian Lotteries

```bash
# Add Asian lotteries to the shared lottery table
poetry run python src/database/populate_lotteries.py
```

This will add 13 Asian lotteries to your existing lottery table.

### 4. Verify Integration

**Check via Next.js API:**
```bash
# See all lotteries (including new Asian ones)
curl http://localhost:3000/api/lotteries

# Should show Powerball, Mega Millions, EuroMillions, EuroJackpot
# PLUS Singapore TOTO, India Kerala, etc.
```

**Check via Python API:**
```bash
# Start Python scraper
cd services/asia-scraper
poetry run python -m src.main

# In another terminal
curl http://localhost:8000/lotteries
```

### 5. Test Scraping

```bash
# Trigger a scrape
curl -X POST http://localhost:8000/scrape/sg-toto

# Check results in Next.js
curl http://localhost:3000/api/lotteries/sg-toto
```

## Database Tables

### Shared Tables (Used by Both Systems)

1. **`lottery`**
   - Written by: Python populate script
   - Read by: Python scraper, Next.js API
   - Contains: All lotteries (US, Europe, Asia)

2. **`result`**
   - Written by: Python scraper
   - Read by: Next.js API, Frontend
   - Contains: Draw results for all lotteries

### Python-Only Tables

3. **`scraper_job`**
   - Tracks scraper execution status
   - Used for monitoring and debugging

4. **`scraper_config`**
   - Stores CRON schedules
   - Manages scraper configuration

### Next.js-Only Tables

- `user`, `account`, `session` - Authentication
- `subscription` - User subscriptions

## Data Flow

```
Python Scraper
    ↓
Populates: lottery table (one-time)
    ↓
Scrapes: External lottery websites
    ↓
Saves to: result table
    ↓
Next.js API reads from: lottery + result tables
    ↓
Frontend displays: All lottery data
```

## Troubleshooting

### Issue: Lotteries not showing in Next.js

**Solution:**
```bash
# Re-run population script
cd services/asia-scraper
poetry run python src/database/populate_lotteries.py
```

### Issue: Results not appearing

**Check:**
1. Scraper ran successfully
2. No duplicate prevention (check drawDate)
3. Lottery isActive = true

```sql
-- Check recent results
SELECT l.name, r."drawDate", r.numbers, r.jackpot
FROM lottery l
JOIN result r ON l.id = r."lotteryId"
ORDER BY r."createdAt" DESC
LIMIT 10;
```

### Issue: UUID errors

Make sure SQLAlchemy model uses:
```python
from sqlalchemy.dialects.postgresql import UUID
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
```

## Benefits of Integration

✅ **Single Source of Truth**: One lottery table for all systems
✅ **Automatic Updates**: Python scrapes → Next.js shows immediately  
✅ **No Duplication**: Shared data, no sync issues  
✅ **Unified API**: Frontend queries one consistent API  
✅ **Scalable**: Easy to add more lotteries or countries

## Next Steps

1. Run migration (see steps above)
2. Test one scraper (e.g., Singapore TOTO)
3. Verify data appears in Next.js
4. Deploy both services
5. Schedule CRON jobs for automatic scraping
