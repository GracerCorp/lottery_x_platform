import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Globe, TrendingUp } from "lucide-react";
import { SubscribeDialog } from "./subscribe-dialog";
import { CountdownTimer } from "./countdown-timer";

interface LotteryProps {
  name: string;
  country: string;
  jackpot: string;
  nextDraw: string;
  tags?: string[];
  logo?: string;
}

export function LotteryCard({
  name,
  country,
  jackpot,
  nextDraw,
  tags,
  logo,
}: LotteryProps) {
  // Mock hot numbers for FOMO effect
  const hotNumbers = [7, 21, 34, 42, 59];

  // Determine glow color based on jackpot amount
  const getGlowColor = () => {
    const amount = parseInt(jackpot.replace(/[^0-9]/g, ""));
    if (amount > 100) return "hover:shadow-amber-500/50";
    if (amount > 50) return "hover:shadow-blue-500/50";
    return "hover:shadow-purple-500/50";
  };

  return (
    <Card
      className={`group hover:-translate-y-2 hover:shadow-2xl ${getGlowColor()} transition-all duration-500 border-zinc-800 bg-zinc-900/50 backdrop-blur-sm overflow-hidden relative`}
    >
      {/* Animated gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 via-transparent to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

      <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2 relative z-10">
        <div className="space-y-1">
          <CardTitle className="text-xl font-bold flex items-center gap-2 text-white">
            {name}
            <Badge
              variant="outline"
              className="text-xs font-normal border-amber-500/50 text-amber-400"
            >
              {country}
            </Badge>
          </CardTitle>
          <div className="text-sm text-muted-foreground flex items-center gap-1">
            <Globe className="h-3 w-3" />
            {currencyForCountry(country)}
          </div>
        </div>
        <div className="bg-gradient-to-br from-amber-500/20 to-yellow-500/20 rounded-full p-2 shadow-lg shadow-amber-500/20 w-12 h-12 flex items-center justify-center">
          {logo ? (
            <img
              src={logo}
              alt={`${name} logo`}
              className="w-8 h-8 object-contain"
              onError={(e) => {
                // Fallback to emoji if image fails to load
                e.currentTarget.style.display = "none";
                e.currentTarget.nextElementSibling?.classList.remove("hidden");
              }}
            />
          ) : null}
          <span className={`text-2xl ${logo ? "hidden" : ""}`}>💰</span>
        </div>
      </CardHeader>
      <CardContent className="relative z-10">
        <div className="space-y-4">
          <div>
            <p className="text-sm font-medium text-zinc-400">
              Estimated Jackpot
            </p>
            <p className="text-4xl font-extrabold bg-gradient-to-r from-amber-400 via-yellow-300 to-amber-500 bg-clip-text text-transparent animate-pulse">
              {jackpot}
            </p>
          </div>

          {/* Countdown Timer */}
          <div className="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700/50">
            <p className="text-xs text-zinc-400 mb-2">Next Draw In:</p>
            <CountdownTimer targetDate={nextDraw} className="justify-center" />
          </div>

          {/* Hot Numbers - FOMO Element */}
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-red-400" />
            <span className="text-xs text-zinc-400">Hot Numbers:</span>
            <div className="flex gap-1">
              {hotNumbers.slice(0, 5).map((num) => (
                <span
                  key={num}
                  className="text-xs font-mono bg-red-500/20 text-red-400 px-1.5 py-0.5 rounded border border-red-500/50"
                >
                  {num}
                </span>
              ))}
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            {tags?.map((tag) => (
              <Badge
                key={tag}
                variant="secondary"
                className="text-xs bg-zinc-800 border-zinc-700 text-zinc-300"
              >
                {tag}
              </Badge>
            ))}
          </div>
        </div>
      </CardContent>
      <CardFooter className="pt-2 relative z-10">
        <SubscribeDialog lotteryName={name} />
      </CardFooter>
    </Card>
  );
}

function currencyForCountry(country: string) {
  if (country === "USA") return "USD";
  if (country === "Europe") return "EUR";
  if (country === "UK") return "GBP";
  return "Global";
}
