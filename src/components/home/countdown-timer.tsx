"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";
import { Clock } from "lucide-react";

interface CountdownTimerProps {
  targetDate: string;
  className?: string;
}

export function CountdownTimer({ targetDate, className }: CountdownTimerProps) {
  const [timeLeft, setTimeLeft] = useState<{
    days: number;
    hours: number;
    minutes: number;
    seconds: number;
  } | null>(null);

  useEffect(() => {
    const calculateTimeLeft = () => {
      const difference = +new Date(targetDate) - +new Date();
      let newTimeLeft = { days: 0, hours: 0, minutes: 0, seconds: 0 };

      if (difference > 0) {
        newTimeLeft = {
          days: Math.floor(difference / (1000 * 60 * 60 * 24)),
          hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
          minutes: Math.floor((difference / 1000 / 60) % 60),
          seconds: Math.floor((difference / 1000) % 60),
        };
      } else {
        // Handle expiration (optional: could trigger refresh or show "Drawing Now")
      }

      setTimeLeft(newTimeLeft);
    };

    calculateTimeLeft();
    const timer = setInterval(calculateTimeLeft, 1000);

    return () => clearInterval(timer);
  }, [targetDate]);

  if (!timeLeft) {
    return null; // or a loading skeleton
  }

  const TimeUnit = ({ value, label }: { value: number; label: string }) => (
    <div className="flex flex-col items-center mx-2 sm:mx-4">
      <div className="relative">
        <div className="w-16 h-16 sm:w-20 sm:h-20 flex items-center justify-center bg-zinc-900/80 backdrop-blur-sm rounded-xl border border-white/10 shadow-xl overflow-hidden">
          {/* Glossy overlay */}
          <div className="absolute inset-x-0 top-0 h-1/2 bg-gradient-to-b from-white/10 to-transparent pointer-events-none" />

          <span className="text-3xl sm:text-4xl font-bold font-mono text-white tabular-nums drop-shadow-md">
            {value.toString().padStart(2, "0")}
          </span>
        </div>
      </div>
      <span className="text-xs sm:text-sm text-zinc-400 mt-2 font-medium tracking-wide uppercase">
        {label}
      </span>
    </div>
  );

  return (
    <div
      className={cn(
        "flex flex-col items-start animate-fade-in-up delay-100",
        className,
      )}
    >
      <div className="flex items-center gap-2 mb-4 text-amber-500 font-bold uppercase tracking-widest text-sm animate-pulse">
        <Clock className="w-4 h-4" />
        <span>Next Draw In</span>
      </div>
      <div className="flex items-center">
        <TimeUnit value={timeLeft.days} label="Days" />
        <span className="text-2xl sm:text-4xl font-bold text-zinc-600 mb-6">
          :
        </span>
        <TimeUnit value={timeLeft.hours} label="Hours" />
        <span className="text-2xl sm:text-4xl font-bold text-zinc-600 mb-6">
          :
        </span>
        <TimeUnit value={timeLeft.minutes} label="Mins" />
        <span className="text-2xl sm:text-4xl font-bold text-zinc-600 mb-6">
          :
        </span>
        <TimeUnit value={timeLeft.seconds} label="Secs" />
      </div>
    </div>
  );
}
