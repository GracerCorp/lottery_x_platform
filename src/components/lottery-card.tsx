"use client";

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
    <Card className="group hover:-translate-y-1 transition-all duration-300 border-zinc-800 bg-zinc-900/90 backdrop-blur-sm overflow-hidden">
      <CardHeader className="pb-1">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              {logo ? (
                <img
                  src={logo}
                  alt={`${name} logo`}
                  className="h-14 object-contain"
                  onError={(e) => {
                    e.currentTarget.style.display = "none";
                  }}
                />
              ) : (
                <CardTitle className="text-lg font-bold text-white">
                  {name}
                </CardTitle>
              )}

              
            </div>
            <div className="flex items-center gap-1.5 text-xs text-zinc-400 mt-4">
              <Badge
                variant="outline"
                className="text-xs border-amber-500/50 text-amber-400 bg-amber-500/10"
              >
                {country}
              </Badge>
              <span>{name}</span>
            </div>
          </div>

          {/* Country Flag */}
          <div className="relative w-14 h-14 flex-shrink-0">
            <div className="absolute inset-0 bg-gradient-to-br from-amber-500/20 to-yellow-600/20 rounded-full blur-lg" />
            <div className="relative w-full h-full bg-gradient-to-br from-amber-500/10 to-yellow-600/10 rounded-full flex items-center justify-center border border-amber-500/20">
              <span className="text-3xl">{getCountryFlag(country)}</span>
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4 pb-4">
        {/* Jackpot */}
        <div>
          <p className="text-xs text-zinc-500 mb-1">Estimated Jackpot</p>
          <p className="text-4xl font-black bg-gradient-to-r from-amber-300 via-yellow-400 to-amber-300 bg-clip-text text-transparent">
            {jackpot}
          </p>
        </div>

        {/* Countdown Timer */}
        <div className="bg-zinc-800/50 rounded-lg p-3 border border-zinc-700/50">
          <p className="text-xs text-zinc-400 mb-2.5">Next Draw In:</p>
          <CountdownTimer targetDate={nextDraw} className="justify-start" />
        </div>

        {/* Hot Numbers */}
        <div>
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="h-3.5 w-3.5 text-red-400" />
            <span className="text-xs text-zinc-400">Hot Numbers:</span>
          </div>
          <div className="flex gap-1.5">
            {hotNumbers.map((num) => (
              <span
                key={num}
                className="text-xs font-mono bg-red-500/20 text-red-400 px-2 py-1 rounded border border-red-500/50 min-w-[32px] text-center"
              >
                {num}
              </span>
            ))}
          </div>
        </div>
      </CardContent>

      <CardFooter className="pt-0 pb-4 ">
        <SubscribeDialog lotteryName={name}/>
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

function getCountryFlag(country: string): string {
  if (country === "USA") return "🇺🇸";
  if (country === "Europe") return "🇪🇺";
  if (country === "UK") return "🇬🇧";
  return "🌍";
}
