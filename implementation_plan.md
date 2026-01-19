# Implementation Plan - PWA & Push Notifications

## Goal Description
Turn the application into a Progressive Web App (PWA) to allow installation on devices and enable push notifications for lottery results. Fix specific issue with missing `service-worker.js`.

## User Review Required
- [ ] Confirm VAPID keys generation approach (will generate and store in `.env.local` for now).

## Proposed Changes

### Configuration
#### [NEW] [public/manifest.json](file:///Users/apinan/Developments/lottery_x_platform/public/manifest.json)
- Define app name, icons, start URL, background color, display mode (standalone).

#### [NEW] [public/sw.js](file:///Users/apinan/Developments/lottery_x_platform/public/sw.js)
-  Basic service worker for offline caching (optional but good practice) and push event handling.

### Components
#### [NEW] [src/components/pwa-install-prompt.tsx](file:///Users/apinan/Developments/lottery_x_platform/src/components/pwa-install-prompt.tsx)
- A component to capture the `beforeinstallprompt` event and show a custom install button.

#### [NEW] [src/components/push-subscription.tsx](file:///Users/apinan/Developments/lottery_x_platform/src/components/push-subscription.tsx)
-   UI to request notification permission and subscribe the user.
-   Will use `web-push` library.

### App Setup
#### [MODIFY] [src/app/layout.tsx](file:///Users/apinan/Developments/lottery_x_platform/src/app/layout.tsx)
-   Register the service worker on mount.
-   Link the manifest file.

### Backend
#### [NEW] [src/app/api/push/subscribe/route.ts](file:///Users/apinan/Developments/lottery_x_platform/src/app/api/push/subscribe/route.ts)
-   Endpoint to save the push subscription (mock or DB).

#### [NEW] [src/components/navbar.tsx](file:///Users/apinan/Developments/lottery_x_platform/src/components/navbar.tsx)
-   Responsive navigation bar with mobile menu (using Sheet).
-   Links to Home, Results, My Tickets.
-   Login/Sign Up actions.

-   Links to Home, Results, My Tickets.
-   Login/Sign Up actions.

#### [NEW] [src/app/results/page.tsx](file:///Users/apinan/Developments/lottery_x_platform/src/app/results/page.tsx)
-   List all lotteries with their latest winning numbers.
-   Grid layout with clearer result balls.
-   "Load More" or simple pagination if needed (start with all).

#### [NEW] [src/app/api/push/send/route.ts](file:///Users/apinan/Developments/lottery_x_platform/src/app/api/push/send/route.ts)
-   Endpoint to trigger a notification (for testing).

## Verification Plan
### Manual Verification
1.  **SW Load**: Check DevTools > Application > Service Workers to see `sw.js` active.
2.  **Install**: Verify "Install App" button appears and functions (on supported browsers like Chrome).
3.  **Notifications**: Click "Subscribe", then trigger a test notification via API/button and verify it appears.

### Push Subscription Persistence
#### [MODIFY] src/db/schema.ts
- Create `pushSubscriptions` table to store Web Push subscription details:
  - `id` (UUID, PK)
  - `endpoint` (Text, Unique) - The URL for the push service.
  - `p256dh` (Text) - User public encryption key.
  - `auth` (Text) - User authentication secret.
  - `userId` (Text, Optional) - To link to a logged-in user if available.
  - `createdAt` (Timestamp)

#### [MODIFY] src/app/api/push/subscribe/route.ts
- Import `db` and `pushSubscriptions` schema.
- Implement `POST` handler to insert subscription data into the `pushSubscriptions` table.
- Update logic to handle duplicate subscriptions (upsert or ignore).
