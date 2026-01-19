export function formatJackpot(
  amount: number,
  currency: string = "USD",
): string {
  const symbols: Record<string, string> = {
    USD: "$",
    EUR: "€",
    GBP: "£",
  };

  const symbol = symbols[currency] || currency;

  if (amount >= 1_000_000_000) {
    return `${symbol}${(amount / 1_000_000_000).toFixed(1)}B`;
  }
  if (amount >= 1_000_000) {
    return `${symbol}${Math.floor(amount / 1_000_000)}M`;
  }
  if (amount >= 1_000) {
    return `${symbol}${Math.floor(amount / 1_000)}K`;
  }
  return `${symbol}${amount}`;
}

export function calculateNextDraw(
  frequency: string,
  baseDate: Date = new Date(),
): Date {
  // Parse frequency like "Mon, Wed, Sat" or "Tue, Fri"
  const days: Record<string, number> = {
    Sun: 0,
    Mon: 1,
    Tue: 2,
    Wed: 3,
    Thu: 4,
    Fri: 5,
    Sat: 6,
  };

  const drawDays = frequency.split(",").map((d) => days[d.trim()]);
  const today = baseDate.getDay();

  // Find next draw day
  let daysUntilNext = 7; // Default to next week
  for (const day of drawDays.sort((a, b) => a - b)) {
    const diff = (day - today + 7) % 7;
    if (diff > 0 && diff < daysUntilNext) {
      daysUntilNext = diff;
    }
  }

  // If no upcoming day this week, use first draw day next week
  if (daysUntilNext === 7) {
    daysUntilNext = (drawDays[0] - today + 7) % 7 || 7;
  }

  const nextDraw = new Date(baseDate);
  nextDraw.setDate(nextDraw.getDate() + daysUntilNext);
  nextDraw.setHours(20, 0, 0, 0); // Default to 8 PM

  return nextDraw;
}

export function generateHotNumbers(
  count: number = 5,
  max: number = 69,
): number[] {
  // Generate mock "hot" numbers (in production, this would use statistical data)
  const numbers: number[] = [];
  const commonNumbers = [7, 21, 32, 41, 42, 16, 23, 35, 59, 62]; // Common lottery numbers

  for (let i = 0; i < count && i < commonNumbers.length; i++) {
    if (commonNumbers[i] <= max) {
      numbers.push(commonNumbers[i]);
    }
  }

  // Fill remaining with random numbers if needed
  while (numbers.length < count) {
    const num = Math.floor(Math.random() * max) + 1;
    if (!numbers.includes(num)) {
      numbers.push(num);
    }
  }

  return numbers.sort((a, b) => a - b);
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/--+/g, "-")
    .trim();
}
