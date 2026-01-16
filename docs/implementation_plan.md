# Global Lottery Platform - Implementation Plan

## Project Goal
Build a global lottery website that displays lottery results from around the world, allows user management (social/mobile login), supports lottery subscriptions, sends push notifications/emails, and is highly SEO optimized.

## User Review Required
> [!IMPORTANT]
> **Tech Stack Validation & Adjustments**
> I have reviewed your proposed stack. Here are my recommendations:
> 1.  **Databases**: You proposed both **PostgreSQL [Neon]** and **MongoDB [Atlas]**.
>     *   *Recommendation*: Stick to **PostgreSQL** (Neon) as the primary database. It supports JSONB for flexible data (like varying lottery result formats) and relational data (users, subscriptions) excellently. Using two databases adds unnecessary complexity for this scale initially.
> 2.  **Deployment**: You mentioned **Docker [Vercel]**.
>     *   *Clarification*: Vercel is a serverless platform optimized for Next.js. You typically deploy the Next.js app directly to Vercel, not a Docker container. Docker is great for local development or if you were hosting on a VPS (like DigitalOcean/AWS EC2).
>     *   *Recommendation*: Deploy directly to **Vercel** for the frontend/API.
> 3.  **Cronjobs**: You mentioned **VPS cronjob**.
>     *   *Recommendation*: Vercel has built-in **[Vercel Cron Jobs](https://vercel.com/docs/cron-jobs)**. This avoids paying for and managing a separate VPS just for crons. Alternatively, simple robust cron services (like Inngest or specialized cron providers) work well with serverless.
> 4.  **Auth**: For login (Social + Mobile), I recommend **Auth.js (NextAuth)**. It handles standard OAuth providers easily. For "Mobile Number" login, we might need a specific provider (like Twilio Verify integration) or a service like Firebase Auth or Supabase Auth which handles SMS well.
> 5.  **Gemini API**: Confirmed. Useful for parsing unstructured lottery results from the web or generating SEO-friendly descriptions.

### Final Recommended Stack
-   **Frontend/Backend**: Next.js 15 (App Router), TailwindCSS, Shadcn/UI (for premium look).
-   **Database**: PostgreSQL (Neon) + Drizzle ORM or Prisma.
-   **Auth**: Auth.js (NextAuth) or Clerk (great for social + phone).
-   **AI**: Gemini API (Data parsing, content generation).
-   **Notifications**:
    -   Email: Postmark (Excellent).
    -   Push: Web Push API (PWA).
-   **Hosting**: Vercel.
-   **Scheduled Tasks**: Vercel Cron or Inngest.

## Proposed Changes

### Phase 1: Foundation & Setup
#### [NEW] [Project Structure]
- Initialize Next.js with TypeScript and TailwindCSS.
- Setup Shadcn/UI for components.
- Configure ESLint/Prettier.

#### [NEW] [Database Setup]
- Initialize Neon PostgreSQL.
- Setup Drizzle ORM (lighter/faster than Prisma) or Prisma.
- Define Schema: `Users`, `Lotteries`, `Results`, `Subscriptions`.

### Phase 2: Core Features
#### [NEW] [User Management]
- Implement Login/Register pages.
- Integrate Auth.js/Clerk.

#### [NEW] [Lottery Data & Display]
- Create "Lotteries" model.
- Build Homepage (Global list).
- Build Single Lottery Page (SEO focused).

### Phase 3: "Smart" Features
#### [NEW] [Gemini Integration]
- Create scripts/functions to fetch raw lottery data and use Gemini to parse/normalize it into our DB format.

#### [NEW] [Notifications]
- Implement Subscription logic.
- Setup Postmark SDK.
- Setup Service Worker for Web Push.

## Verification Plan

### Automated Tests
- Unit tests for data parsing logic (critical for lottery numbers).
- E2E tests for User Login flow.

### Manual Verification
- Testing responsiveness on Mobile.
- Verifying Push Notifications work on supported browsers (Chrome/Safari/Edge).
- Validating SEO tags (OpenGraph, JSON-LD schemas).
