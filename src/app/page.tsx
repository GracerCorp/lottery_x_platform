import { LotteryCard } from "@/components/lottery-card";
import { Button } from "@/components/ui/button";
import { TickerTape } from "@/components/ticker-tape";
import { Sparkles, TrendingUp, Trophy, Globe2 } from "lucide-react";

// Fetch lotteries from API
async function getLotteries() {
  try {
    const baseUrl = process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000";
    const res = await fetch(`${baseUrl}/api/lotteries?limit=4`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch");
    return res.json();
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

export default async function Home() {
  const lotteries = await getLotteries();
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
      {/* Navbar */}
      <header className="sticky top-0 z-50 w-full border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-xl supports-[backdrop-filter]:bg-zinc-950/60">
        <div className="container mx-auto max-w-7xl px-4 flex h-16 items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-2xl">
            <Globe2 className="h-8 w-8 text-amber-500" />
            <span className="bg-gradient-to-r from-amber-400 to-yellow-300 bg-clip-text text-transparent">
              Global
            </span>
            <span className="text-zinc-100">Lotto</span>
          </div>
          <nav className="flex gap-4">
            <Button variant="ghost" className="text-zinc-300 hover:text-white">
              How it works
            </Button>
            <Button className="bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 text-zinc-950 font-semibold">
              Login
            </Button>
          </nav>
        </div>
      </header>

      {/* Live Ticker */}
      <TickerTape items={nextDrawTicker} variant="primary" speed="normal" />

      {/* Hero */}
      <section className="relative py-32 px-4 md:px-8 text-center overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 bg-gradient-to-b from-zinc-950 via-zinc-900 to-zinc-950" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-amber-900/20 via-transparent to-transparent" />

        {/* Floating orbs */}
        <div className="absolute top-20 left-1/4 w-72 h-72 bg-amber-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-20 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000" />

        <div className="relative z-10 space-y-8 max-w-5xl mx-auto px-4">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Sparkles className="h-6 w-6 text-amber-400 animate-pulse" />
            <span className="text-sm font-semibold text-amber-400 uppercase tracking-wider">
              Global Jackpots Await
            </span>
            <Sparkles className="h-6 w-6 text-amber-400 animate-pulse" />
          </div>

          <h1 className="text-6xl md:text-8xl font-black tracking-tight">
            <span className="bg-gradient-to-r from-amber-200 via-yellow-300 to-amber-400 bg-clip-text text-transparent animate-gradient">
              Win the World.
            </span>
          </h1>

          <p className="text-xl md:text-2xl text-zinc-400 max-w-3xl mx-auto leading-relaxed">
            Track the biggest lottery jackpots from{" "}
            <span className="text-amber-400 font-semibold">
              USA, Europe & Asia
            </span>{" "}
            in real-time. Never miss a life-changing draw again.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-6">
            <Button
              size="lg"
              className="text-lg px-10 h-14 rounded-full bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 text-zinc-950 font-bold shadow-2xl shadow-amber-500/50"
            >
              Explore Lotteries
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="text-lg px-10 h-14 rounded-full border-2 border-zinc-700 hover:border-amber-500 hover:text-amber-400"
            >
              How It Works
            </Button>
          </div>

          {/* Trust signals */}
          <div className="flex items-center justify-center gap-8 pt-8 text-sm text-zinc-500">
            <div className="flex items-center gap-2">
              <Trophy className="h-5 w-5 text-amber-500" />
              <span>Verified Results</span>
            </div>
            <div className="flex items-center gap-2">
              <Globe2 className="h-5 w-5 text-blue-500" />
              <span>50+ Countries</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-green-500" />
              <span>Real-time Updates</span>
            </div>
          </div>
        </div>
      </section>

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
          {lotteries.map((lottery: any) => (
            <LotteryCard
              key={lottery.id}
              name={lottery.name}
              country={lottery.country}
              jackpot={lottery.jackpot}
              nextDraw={lottery.nextDraw}
              logo={lottery.logo}
              tags={lottery.tags}
            />
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-zinc-800 py-12 bg-zinc-950 text-center text-sm text-zinc-500">
        <p>&copy; 2026 Global Lottery Platform. All rights reserved.</p>
      </footer>
    </div>
  );
}
