import { Button } from "@/components/ui/button";
import { NumberChecker } from "./number-checker";
import { CountdownTimer } from "./countdown-timer";
import { Sparkles, ArrowRight } from "lucide-react";
import Link from "next/link";

interface HeroSectionProps {
  featuredLottery: {
    id: string;
    name: string;
    jackpot: string;
    nextDraw: string;
    country: string;
    logo?: string | null;
  } | null;
  allLotteries: {
    id: string;
    name: string;
    latestResult?: {
      numbers: { main: number[]; bonus: number[] };
      drawDate: string;
    };
  }[];
}

export function HeroSection({
  featuredLottery,
  allLotteries,
}: HeroSectionProps) {
  if (!featuredLottery) {
    return (
      <section className="relative py-20 min-h-[600px] flex items-center justify-center bg-zinc-950 overflow-hidden">
        <div className="text-center space-y-4 relative z-10 p-4">
          <h1 className="text-5xl font-bold text-white mb-4">
            Global Lotteries
          </h1>
          <p className="text-zinc-400">
            Discover huge jackpots from around the world.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="relative min-h-[80vh] flex items-center justify-center bg-zinc-950 overflow-hidden pt-20 pb-20">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-amber-900/20 via-zinc-950 to-zinc-950" />
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-7xl overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-amber-500/10 rounded-full blur-[100px] animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-purple-500/10 rounded-full blur-[120px] animate-pulse delay-700" />
      </div>

      <div className="container mx-auto sm:max-w-100 md:max-w-7xl px-4 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Text Content */}
          <div className="text-center lg:text-left space-y-8">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 animate-fade-in-up">
              <Sparkles className="w-4 h-4" />
              <span className="text-sm font-bold tracking-wide uppercase">
                Top Jackpot
              </span>
            </div>

            <div className="space-y-4">
              <h1 className="text-6xl md:text-8xl font-black tracking-tight text-white leading-[0.9]">
                <span className="block text-zinc-500 text-4xl md:text-5xl font-bold mb-2 tracking-normal">
                  {featuredLottery.name}
                </span>
                <span className="bg-gradient-to-r from-amber-200 via-yellow-400 to-amber-500 bg-clip-text text-transparent drop-shadow-2xl">
                  {featuredLottery.jackpot}
                </span>
              </h1>

              <CountdownTimer
                targetDate={featuredLottery.nextDraw}
                className="justify-center lg:justify-start scale-90 sm:scale-100 origin-top"
              />

              <p className="text-xl text-zinc-400 max-w-lg mx-auto lg:mx-0">
                The world's biggest prize is waiting.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Button
                asChild
                size="lg"
                className="h-14 px-8 text-lg rounded-full bg-amber-500 hover:bg-amber-600 text-black font-bold shadow-lg shadow-amber-500/20 transition-all hover:scale-105"
              >
                <Link
                  href={`/lottery/${featuredLottery.name.toLowerCase().replace(/\s+/g, "-")}`}
                >
                  Play Now <ArrowRight className="ml-2 w-5 h-5" />
                </Link>
              </Button>
              <Button
                asChild
                variant="outline"
                size="lg"
                className="h-14 px-8 text-lg rounded-full border-zinc-800 text-amber-600 hover:text-white hover:border-zinc-700 hover:bg-zinc-900/50"
              >
                <Link href="/results">View Past Results</Link>
              </Button>
            </div>
          </div>

          {/* Interactive Tool */}
          <div className="flex justify-center lg:justify-end animate-fade-in-up delay-200">
            <NumberChecker lotteries={allLotteries} />
          </div>
        </div>
      </div>
    </section>
  );
}
