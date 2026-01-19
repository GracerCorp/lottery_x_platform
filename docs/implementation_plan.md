# UI/UX Overhaul & FOMO Implementation Plan

## Goal Description
Transform the "Lottery X Platform" into a high-energy, premium experience ("Win the World") that instills FOMO (Fear Of Missing Out) and excitement. The design will follow the guidelines in `docs/ui_ux_design.md`: dark mode preference, vibrant accents, animated tickers, and "glow" effects.

## User Review Required
> [!IMPORTANT]
> The design will heavily shift towards a **Dark Mode** first aesthetic. Light mode might be secondary or removed if a purely "Premium Dark" feel is desired as per the design doc (implied by "Deep Zinc/Slate backgrounds").

## Proposed Changes

### Components Layer [`src/components`]
#### [NEW] `src/components/countdown-timer.tsx`
- A reusable component that takes a target date and animates the time remaining (Days : Hours : Mins : Secs).
- Uses monospace font for numbers.

#### [NEW] `src/components/ticker-tape.tsx`
- A scrolling marquee component (using CSS animations).
- Used for "Next Big Draw" and "Recent Winners".

#### [MODIFY] `src/components/lottery-card.tsx`
- **Visuals**: Add hover lift effect (`hover:-translate-y-2`), colored glow shadows based on lottery type (Gold/Blue).
- **Features**: Add the `CountdownTimer` and a "Subscribe" bell icon button.
- **Data**: Display "Hot/Cold" numbers (mocked for now).

### Page Layer [`src/app`]
#### [MODIFY] `src/app/page.tsx`
- **Hero Section**:
    - Replace basic white/gray gradient with deep `zinc-950` and energetic gradients.
    - Add "Win the World" typography with gradient text.
    - Insert `TickerTape` at the top or below nav.
- **Grid Section**:
    - Update background to dark tint.
    - Improve section headers.
- **Footer**:
    - Dark mode styling.

#### [MODIFY] `src/app/globals.css`
- Ensure `@custom-variant dark` is working or manually enforce dark classes if we stick to one theme.
- Add specific keyframes for `ticker` animation if not present in `tw-animate-css`.

## Verification Plan

### Automated Tests
- None currently exist for UI visuals.
- Run `npm run dev` and navigate to `http://localhost:3000`.

### Manual Verification
1.  **Visual Check**:
    -   Does the Hero section look premiums? (Dark bg, gradient text).
    -   Do the tickers scroll smoothly?
    -   Do cards lift on hover?
2.  **Functional Check**:
    -   Does the Countdown timer tick down?
    -   Does the "Subscribe" button click (console log is fine for now)?
3.  **Responsive Check**:
    -   Ensure tickers works on mobile.
    -   Grid layout adjusts correctly.
