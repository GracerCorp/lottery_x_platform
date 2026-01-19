# Database & API Implementation Walkthrough

## Overview
Successfully implemented a complete database and API infrastructure for the Lottery X Platform using Drizzle ORM and Next.js API routes.

## What Was Created

### 1. Database Layer

#### Database Connection
[src/db/index.ts](file:///Users/apinan/Developments/lottery_x_platform/src/db/index.ts)
- PostgreSQL connection pool using `pg`
- Drizzle ORM instance with schema
- Singleton pattern for efficient connection reuse

#### Seed Script
[src/db/seed.ts](file:///Users/apinan/Developments/lottery_x_platform/src/db/seed.ts)
- Seeds 4 major lotteries: Powerball, Mega Millions, EuroMillions, EuroJackpot
- Creates 2 result entries per lottery (upcoming draw + past draw)
- Dynamic jackpot calculation using utility functions

---

### 2. Utility Functions

[src/lib/lottery.ts](file:///Users/apinan/Developments/lottery_x_platform/src/lib/lottery.ts)

**Functions Created:**
- `formatJackpot(amount, currency)`: Formats numbers into readable currency (e.g., $245M, €164M)
- `calculateNextDraw(frequency, baseDate)`: Calculates next draw date based on draw frequency
- `generateHotNumbers(count, max)`: Generates mock "hot" lottery numbers
- `slugify(text)`: Creates URL-friendly slugs

---

### 3. API Routes

#### GET /api/lotteries
[src/app/api/lotteries/route.ts](file:///Users/apinan/Developments/lottery_x_platform/src/app/api/lotteries/route.ts)

**Purpose**: Fetch all active lotteries with latest jackpot information

**Query Parameters:**
- `limit` (optional): Number of results (default: 10)
- ~~`country` (planned for v2)~~

**Response Example:**
```json
[
  {
    "id": "uuid",
    "name": "Powerball",
    "slug": "powerball-usa",
    "country": "USA",
    "jackpot": "$245M",
    "nextDraw": "2026-01-22T20:00:00.000Z",
    "currency": "USD"
  }
]
```

#### GET /api/lotteries/[slug]
[src/app/api/lotteries/[slug]/route.ts](file:///Users/apinan/Developments/lottery_x_platform/src/app/api/lotteries/[slug]/route.ts)

**Purpose**: Fetch single lottery details with recent results

**Response Example:**
```json
{
  "lottery": { /* lottery object */ },
  "results": [
    {
      "drawDate": "2026-01-22T20:00:00.000Z",
      "numbers": {"main": [7,21,32,41,42], "bonus": [16]},
      "jackpot": "$245M",
      "winners": [...]
    }
  ]
}
```

#### GET /api/results
[src/app/api/results/route.ts](file:///Users/apinan/Developments/lottery_x_platform/src/app/api/results/route.ts)

**Purpose**: Fetch lottery results across all or specific lotteries

**Query Parameters:**
- `lotteryId` (optional): Filter by lottery UUID
- `limit` (optional): Number of results (default: 10)

---

### 4. Frontend Integration

#### Updated Homepage
[src/app/page.tsx](file:///Users/apinan/Developments/lottery_x_platform/src/app/page.tsx#L6-L34)

**Changes:**
- ✅ Converted to **async Server Component**
- ✅ Fetches lotteries from `/api/lotteries` on every request
- ✅ Dynamically generates ticker data from API response
- ✅ Fallback to empty array if API fails

**Before:** Static mock data  
**After:** Real-time database queries

---

## Database Schema

The existing Drizzle schema (`src/db/schema.ts`) includes:

### Tables Created
1. **lottery**: Stores lottery information (name, country, frequency, etc.)
2. **result**: Stores draw results (numbers, jackpots, winners)
3. **subscription**: User subscriptions to lotteries
4. **user**, **account**, **session**: Authentication (NextAuth.js)

---

## Setup Instructions

### 1. Configure Database
Create `.env.local` with your PostgreSQL connection:
```bash
DATABASE_URL="postgresql://user:password@localhost:5432/lottery_db"
```

### 2. Install Dependencies
```bash
npm install tsx --save-dev
```

### 3. Push Schema to Database
```bash
npm run db:push
```

### 4. Seed Database
```bash
npm run db:seed
```

### 5. Verify Data
Open Drizzle Studio to inspect the database:
```bash
npm run db:studio
```

---

## Available NPM Scripts

Added to `package.json`:
- `db:generate` - Generate migrations from schema
- `db:push` - Push schema changes to database (no migration files)
- `db:studio` - Open Drizzle Studio GUI
- `db:seed` - Run seed script to populate initial data

---

## Verification Results

### Lint Status
```bash
npm run lint
```
✅ **0 Errors**  
⚠️ **1 Warning**: Unused `country` parameter (planned for v2 filtering)

### API Testing
Test endpoints using:
```bash
# Fetch all lotteries
curl http://localhost:3000/api/lotteries?limit=4

# Fetch specific lottery
curl http://localhost:3000/api/lotteries/powerball-usa

# Fetch results
curl http://localhost:3000/api/results?limit=10
```

---

## Next Steps

### Required Before Production
1. **Set DATABASE_URL** in environment variables
2. **Run migrations**: `npm run db:push`
3. **Seed database**: `npm run db:seed`
4. **Test API endpoints** to ensure data exists

### Future Enhancements (v2)
- Add country filtering to `/api/lotteries`
- Implement `/api/subscriptions` endpoints (requires authentication)
- Add real lottery number analysis (replace mock hot numbers)
- Implement scheduled jobs to fetch latest results from external APIs
- Add caching layer (Redis) for frequently accessed data

---

## Files Modified

| File | Type | Purpose |
|------|------|---------|
| `src/db/index.ts` | NEW | Database connection |
| `src/db/seed.ts` | NEW | Database seeding |
| `src/lib/lottery.ts` | NEW | Utility functions |
| `src/app/api/lotteries/route.ts` | NEW | GET all lotteries |
| `src/app/api/lotteries/[slug]/route.ts` | NEW | GET lottery by slug |
| `src/app/api/results/route.ts` | NEW | GET results |
| `src/app/page.tsx` | MODIFIED | Async server component |
| `package.json` | MODIFIED | Added db scripts |
