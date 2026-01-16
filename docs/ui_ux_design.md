# Global Lottery Platform - UI/UX Design Document

## 1. Executive Summary
This document outlines the User Interface (UI) and User Experience (UX) strategy for the Global Lottery Platform. The goal is to create a seamless, premium, and trustworthy experience for users to track global lotteries and manage subscriptions.

## 2. User Personas

### Primary: "Global Gary" (The High-Roller)
- **Profile**: 35-year-old tech-savvy professional, dreams of financial freedom.
- **Goals**: Wants to see big jackpots from US, Europe, and Asia in one place. Wants to be notified immediately if he wins or if a jackpot hits a certain threshold.
- **Pain Points**: Current sites are cluttered, ads-heavy, and region-locked.

### Secondary: "Casual Casey" (The Dreamer)
- **Profile**: 28-year-old gig worker, plays occasionally when news mentions "Record Jackpot".
- **Goals**: Quick, frictionless entry. Doesn't want to create an account unless necessary.
- **Pain Points**: Confused by complex odds or multiple draw days. Just wants to know "How much can I win?" and "Where do I buy?".

### Tertiary: "Syndicate Sam" (The Organizer)
- **Profile**: 45-year-old office manager running the company lottery pool.
- **Goals**: Needs to track multiple tickets for different lotteries. Needs shareable results to send to the group.
- **Pain Points**: Manual checking of 50+ numbers is tedious and prone to error.


## 3. Core User Journey

### Phase 1: Discovery & Awe (The "Hook")
**Goal**: User lands on the site and immediately understands value + feels excited.
1.  **Landing Page**:
    -   **Hero Section**: Dynamic background with a subtle globe animation. Huge, bold text: "Win the World."
    -   **Ticker**: A live-updating ticker tape showing the next big draw (e.g., "Powerball: $450M - 2h 15m remaining").
    -   **Trust Signals**: "Verified Results", "Global Coverage".

### Phase 2: Exploration (The "Hunt")
**Goal**: Find specific lotteries or browse by highest jackpot.
1.  **Lottery Grid (Homepage)**:
    -   Card-based layout (Masonry style).
    -   **Sorting**: Toggle between "Highest Jackpot", "Next Draw", "Ending Soon".
    -   **Search**: Instant search bar for "Powerball", "EuroMillions".
2.  **Lottery Detail Page**:
    -   Clicking a card opens a dedicated page/modal.
    -   **Visuals**: High-res logo of the lottery.
    -   **Stats**: Historical winning numbers, "Hot" and "Cold" numbers (AI-generated insights).
    -   **Countdown**: Big, clear countdown timer to next draw.

### Phase 3: Commitment (The "Action")
**Goal**: Subscribe to notifications.
1.  **Subscription Flow**:
    -   User clicks "Subscribe" bell icon on a card.
    -   **Scenario A (Not Logged In)**:
        -   Prompt: "Login to save preferences".
        -   Social Login (Google/GitHub) or "One-tap" Phone login.
    -   **Scenario B (Logged In)**:
        -   **Modal**: "Notify me via:" [x] Email [x] Push.
        -   **Triggers**: "When Jackpot > $100M", "When Results are out".
    -   **Integration**: Browser asks for Notification Permission immediately.

### Phase 4: Retention (The "Loop")
**Goal**: Bring the user back.
1.  **Notification**:
    -   *Push*: "🇺🇸 Powerball Results: 12-45-22... Did you win?"
    -   *Email*: Weekly digest of upcoming massive jackpots.
2.  **Dashboard**:
    -   User profile showing "My Subscriptions".
    -   "Check my Numbers" tool (Manual input to see if they won past draws).

## 4. Information Architecture (Sitemap)

-   **Home (/)**:
    -   Hero / Featured Jackpot
    -   All Lotteries Grid
    -   How it Works
-   **Lottery Detail (/lottery/[slug])**:
    -   Past Results
    -   Next Draw Info
    -   Stats/Analysis
-   **Auth (/login, /register)**:
    -   Social Auth buttons
    -   Phone Number input
-   **User Dashboard (/dashboard)**:
    -   Managed Subscriptions
    -   Notification Settings
-   **Legal**:
    -   Privacy Policy
    -   Terms of Service

## 5. UI Design System Principles
-   **Palette**: Deep Zinc/Slate backgrounds (Dark Mode default?) with Vibrant Accents (Gold/Green for money, Neon Blue for tech).
-   **Typography**: Clean Sans-Serif (Inter/Geist) for readability. Monospace for Numbers (Lottery balls).
-   **Motion**:
    -   *Hover*: Cards lift up and glow.
    -   *Numbers*: Rolling counter animation when jackpots update.
    -   *Transitions*: Smooth page transitions using View Transitions API.

## 6. Step-by-Step UI Flow (Wireframe Description)

### Flow: New User Subscribing to Powerball
1.  **Screen 1: Home**:
    -   User sees "Powerball - $200M" card.
    -   Status: "Draw in 4 hours".
    -   Action: Clicks "Subscribe" (Bell Icon).
2.  **Screen 2: Auth Dialog** (Overlay):
    -   "Sign in to track Powerball".
    -   Action: Clicks "Continue with Google".
3.  **Screen 3: Preference Setup** (Overlay/Modal):
    -   "Successfully Signed in!".
    -   Settings: "Notify me for Results" (Checked by default).
    -   Action: Clicks "Enable Push Notifications".
4.  **Screen 4: Implementation**:
    -   Browser prompt: "Allow Notifications?".
    -   User clicks Allow.
    -   Success Toast: "You're all set! We'll ping you when numbers are out."
