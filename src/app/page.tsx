import { LotteryCard } from "@/components/lottery-card";
import { Button } from "@/components/ui/button";
import { TickerTape } from "@/components/ticker-tape";
import { Sparkles, TrendingUp, Trophy, Globe2 } from "lucide-react";
import { db } from "@/db";
import { lotteries, results } from "@/db/schema";
import { eq, desc } from "drizzle-orm";

// Fetch lotteries directly from database
async function getLotteries() {
  try {
    const data = await db
      .select({
        id: lotteries.id,
        name: lotteries.name,
        slug: lotteries.slug,
        country: lotteries.country,
        region: lotteries.region,
        frequency: lotteries.frequency,
        logo: lotteries.logo,
        description: lotteries.description,
        officialLink: lotteries.officialLink,
      })
      .from(lotteries)
      .where(eq(lotteries.isActive, true))
      .limit(4);

    // Fetch latest result for each lottery to get current jackpot
    const lotteriesWithJackpots = await Promise.all(
      data.map(async (lottery) => {
        const [latestResult] = await db
          .select({
            jackpot: results.jackpot,
            drawDate: results.drawDate,
            currency: results.currency,
          })
          .from(results)
          .where(eq(results.lotteryId, lottery.id))
          .orderBy(desc(results.drawDate))
          .limit(1);

        return {
          ...lottery,
          jackpot: latestResult?.jackpot || "$0",
          nextDraw:
            latestResult?.drawDate?.toISOString() || new Date().toISOString(),
          currency: latestResult?.currency || "USD",
        };
      }),
    );

    return lotteriesWithJackpots;
  } catch (error) {
    console.error("Error fetching lotteries:", error);
    return [];
  }
}

const recentWinnersTicker = [
  { id: "1", text: "Maria K. won", highlight: "$1.2M", icon: "🎉" },
  { id: "2", text: "John D. won", highlight: "€850K", icon: "🏆" },
  { id: "3", text: "Aisha M. won", highlight: "$2.5M", icon: "💎" },
  { id: "4", text: "Chen L. won", highlight: "¥12M", icon: "🌟" },
];

import { HeroSection } from "@/components/home/hero-section";
import { parseJackpotValue } from "@/lib/lottery";

// ... (imports remain)

export default async function Home() {
  const lotteries = await getLotteries();

  // Find top lottery with jackpot > 100M
  const featuredLottery =
    lotteries
      .filter((l) => parseJackpotValue(l.jackpot) >= 100_000_000)
      .sort(
        (a, b) => parseJackpotValue(b.jackpot) - parseJackpotValue(a.jackpot),
      )[0] || null;

  const nextDrawTicker = lotteries.map(
    (lottery: {
      id: string;
      name: string;
      jackpot: string;
      country: string;
    }) => ({
      id: lottery.id,
      text: lottery.name,
      highlight: lottery.jackpot,
      icon: lottery.country === "USA" ? "🇺🇸" : "🇪🇺",
    }),
  );
  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-50">
      {/* Live Ticker */}
      <TickerTape items={nextDrawTicker} variant="primary" speed="normal" />

      {/* Hero */}
      <HeroSection featuredLottery={featuredLottery} allLotteries={lotteries} />

      {/* Recent Winners Ticker */}
      <TickerTape
        items={recentWinnersTicker}
        variant="secondary"
        speed="fast"
      />

      {/* Lottery Grid */}
      <main className="container mx-auto max-w-7xl px-4 py-20">
        <div className="flex items-center justify-between mb-12">
          <div>
            <h2 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-white to-zinc-400 bg-clip-text text-transparent">
              Trending Lotteries
            </h2>
            <p className="text-zinc-500 mt-2">
              Don&apos;t miss out on these massive jackpots
            </p>
          </div>
          <Button
            variant="link"
            className="text-amber-400 hover:text-amber-300"
          >
            View All &rarr;
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {lotteries.map((lottery) => (
            <LotteryCard
              key={lottery.id}
              name={lottery.name}
              country={lottery.country}
              jackpot={lottery.jackpot}
              nextDraw={lottery.nextDraw}
              logo={lottery.logo || undefined}
            />
          ))}
        </div>
      </main>
    </div>
  );
}
