# Global Lottery Platform - Walkthrough

I have successfully built the foundation for the Global Lottery Platform. The project is initialized with a robust tech stack, modern UI, and backend integrations.

## 🚀 Key Features Implemented

### 1. Modern & Premium UI
- **Tech Stack**: Next.js 15, TailwindCSS, Shadcn/UI.
- **Design**: Minimalist, clean aesthetics using `Zinc` palette and `Lucide` icons.
- **Components**:
    - **Lottery Card**: Displays jackpot, country, and next draw.
    - **Subscription Dialog**: Clean interface for Email/Push preferences.
    - **Responsive Layout**: Works perfectly on mobile and desktop.

### 2. Backend & Data
- **Database**: PostgreSQL (Neon) with **Drizzle ORM**.
- **Schema**:
    - `users`: For authentication.
    - `lotteries`: Stores global lottery info.
    - `results`: Stores winning numbers and jackpots.
    - `subscriptions`: User preferences for notifications.

### 3. Authentication
- **Auth.js (NextAuth v5)**: Configured with Google and GitHub providers.
- **Database Adapter**: Automatically persists sessions and users to Postgres.

### 4. Smart Integrations
- **Gemini API**: Set up `src/lib/lottery-parser.ts` to intelligently parse raw lottery text into structured JSON.
- **Web Push**: Added `public/sw.js` foundation for Service Workers.

## 🛠️ Setup Instructions

### 1. Environment Variables
Rename `.env.local` or create it with your real keys:
```bash
DATABASE_URL="postgres://..." # Get from Neon Dashboard
AUTH_SECRET="random-string" # Run `npx auth secret`
AUTH_GOOGLE_ID="..."
AUTH_GOOGLE_SECRET="..."
GEMINI_API_KEY="..." # Get from Google AI Studio
```

### 2. Database Migration
Push the schema to your Neon database:
```bash
npx drizzle-kit push
```

### 3. Running the App
```bash
npm run dev
```
Visit `http://localhost:3000` to see the listing page.

## ✅ Verification
- **Build**: Passed (`npm run build`).
- **Type Safety**: Verified with TypeScript.
- **SEO**: Metadata configured for OpenGraph and Search Engines.

## 🔮 Next Steps
1. **Deploy to Vercel**: Connect this repo to Vercel; it will auto-detect the Next.js config.
2. **Cron Jobs**: Set up a Vercel Cron to hit `/api/cron/update-lottery` (once implemented) to fetch results automatically.
3. **Real Data**: Replace mock data in `page.tsx` with a database query:
   ```typescript
   const lotteries = await db.query.lotteries.findMany();
   ```
