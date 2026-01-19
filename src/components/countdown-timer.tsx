"use client";

import { useEffect, useState } from "react";

interface CountdownTimerProps {
  targetDate: string;
  className?: string;
}

interface TimeRemaining {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
  expired: boolean;
}

export function CountdownTimer({
  targetDate,
  className = "",
}: CountdownTimerProps) {
  const [timeRemaining, setTimeRemaining] = useState<TimeRemaining>({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
    expired: false,
  });

  useEffect(() => {
    const calculateTimeRemaining = () => {
      const now = new Date().getTime();
      const target = new Date(targetDate).getTime();
      const difference = target - now;

      if (difference <= 0) {
        setTimeRemaining({
          days: 0,
          hours: 0,
          minutes: 0,
          seconds: 0,
          expired: true,
        });
        return;
      }

      const days = Math.floor(difference / (1000 * 60 * 60 * 24));
      const hours = Math.floor(
        (difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60),
      );
      const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((difference % (1000 * 60)) / 1000);

      setTimeRemaining({
        days,
        hours,
        minutes,
        seconds,
        expired: false,
      });
    };

    calculateTimeRemaining();
    const interval = setInterval(calculateTimeRemaining, 1000);

    return () => clearInterval(interval);
  }, [targetDate]);

  if (timeRemaining.expired) {
    return <div className={`font-mono text-sm ${className}`}>Draw Ended</div>;
  }

  return (
    <div className={`flex gap-2 items-center font-mono ${className}`}>
      {timeRemaining.days > 0 && (
        <div className="flex flex-col items-center">
          <span className="text-2xl font-bold tabular-nums text-white">
            {String(timeRemaining.days).padStart(2, "0")}
          </span>
          <span className="text-xs text-muted-foreground">Days</span>
        </div>
      )}
      {(timeRemaining.days > 0 || timeRemaining.hours > 0) && (
        <>
          {timeRemaining.days > 0 && <span className="text-2xl">:</span>}
          <div className="flex flex-col items-center">
            <span className="text-2xl font-bold tabular-nums text-white">
              {String(timeRemaining.hours).padStart(2, "0")}
            </span>
            <span className="text-xs text-muted-foreground">Hrs</span>
          </div>
        </>
      )}
      <span className="text-2xl">:</span>
      <div className="flex flex-col items-center">
        <span className="text-2xl font-bold tabular-nums text-white">
          {String(timeRemaining.minutes).padStart(2, "0")}
        </span>
        <span className="text-xs text-muted-foreground">Min</span>
      </div>
      <span className="text-2xl">:</span>
      <div className="flex flex-col items-center">
        <span className="text-2xl font-bold tabular-nums text-white">
          {String(timeRemaining.seconds).padStart(2, "0")}
        </span>
        <span className="text-xs text-muted-foreground">Sec</span>
      </div>
    </div>
  );
}
