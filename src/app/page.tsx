import { LotteryCard } from "@/components/lottery-card";
import { Button } from "@/components/ui/button";

// Mock Data
const lotteries = [
  {
    id: "1",
    name: "Powerball",
    country: "USA",
    jackpot: "$145 Million",
    nextDraw: "2026-01-18",
    frequency: "Mon, Wed, Sat",
    tags: ["High Jackpot", "Popular"]
  },
  {
    id: "2",
    name: "Mega Millions",
    country: "USA",
    jackpot: "$82 Million",
    nextDraw: "2026-01-17",
    frequency: "Tue, Fri",
    tags: ["Global Favorite"]
  },
  {
    id: "3",
    name: "EuroMillions",
    country: "Europe",
    jackpot: "€64 Million",
    nextDraw: "2026-01-17",
    frequency: "Tue, Fri",
    tags: ["Tax Free in UK"]
  },
  {
    id: "4",
    name: "EuroJackpot",
    country: "Europe",
    jackpot: "€120 Million",
    nextDraw: "2026-01-17",
    frequency: "Tue, Fri",
    tags: ["Record High"]
  },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950">
      {/* Navbar */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2 font-bold text-2xl">
            <span className="text-primary">Global</span>Lotto
          </div>
          <nav className="flex gap-4">
            <Button variant="ghost">How it works</Button>
            <Button>Login</Button>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="py-24 px-4 text-center space-y-6 bg-gradient-to-b from-white to-zinc-100 dark:from-zinc-950 dark:to-zinc-900 border-b">
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-zinc-900 to-zinc-600 dark:from-white dark:to-zinc-400">
          Win the World.
        </h1>
        <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto">
          Track and subscribe to the biggest lotteries from across the globe. Never miss a draw again.
        </p>
        <div className="pt-4">
           <Button size="lg" className="text-lg px-8 h-12 rounded-full">Explore Lotteries</Button>
        </div>
      </section>

      {/* Lottery Grid */}
      <main className="container py-16">
        <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold tracking-tight">Trending Lotteries</h2>
            <Button variant="link">View All &rarr;</Button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {lotteries.map((lottery) => (
            <LotteryCard
              key={lottery.id}
              name={lottery.name}
              country={lottery.country}
              jackpot={lottery.jackpot}
              nextDraw={lottery.nextDraw}
              frequency={lottery.frequency}
              tags={lottery.tags}
            />
          ))}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t py-12 bg-white dark:bg-zinc-900 text-center text-sm text-zinc-500">
        <p>&copy; 2026 Global Lottery Platform. All rights reserved.</p>
      </footer>
    </div>
  );
}
