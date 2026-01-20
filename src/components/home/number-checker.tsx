"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Search, Trophy, XCircle } from "lucide-react";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

interface NumberCheckerProps {
  lotteries: {
    id: string;
    name: string;
    latestResult?: {
      numbers: { main: number[]; bonus: number[] };
      drawDate: string;
    };
  }[];
}

export function NumberChecker({ lotteries }: NumberCheckerProps) {
  const [selectedLotteryId, setSelectedLotteryId] = useState<string>("");
  const [userNumbers, setUserNumbers] = useState<string[]>(Array(6).fill(""));
  const [bonusNumber, setBonusNumber] = useState<string>("");
  const [checkResult, setCheckResult] = useState<{
    matches: number;
    bonusMatch: boolean;
    mainMatches: number[];
  } | null>(null);

  const handleNumberChange = (index: number, value: string) => {
    const newNumbers = [...userNumbers];
    // Allow only numeric input
    if (value === "" || /^\d+$/.test(value)) {
      newNumbers[index] = value;
      setUserNumbers(newNumbers);
    }
  };

  const handleCheck = () => {
    if (!selectedLotteryId) {
      toast.error("Please select a lottery");
      return;
    }

    const lottery = lotteries.find((l) => l.id === selectedLotteryId);
    if (!lottery || !lottery.latestResult) {
      toast.error("No result data available for this lottery");
      return;
    }

    const inputMainNumbers = userNumbers
      .map((n) => parseInt(n))
      .filter((n) => !isNaN(n));

    if (inputMainNumbers.length === 0) {
      toast.error("Please enter at least one number");
      return;
    }

    const winningMain = lottery.latestResult.numbers.main;
    const winningBonus = lottery.latestResult.numbers.bonus;

    const MATCHES = inputMainNumbers.filter((n) => winningMain.includes(n));
    const bonusInput = parseInt(bonusNumber);
    const BONUS_MATCH = !isNaN(bonusInput) && winningBonus.includes(bonusInput);

    setCheckResult({
      matches: MATCHES.length,
      bonusMatch: BONUS_MATCH,
      mainMatches: MATCHES,
    });
  };

  return (
    <Card className="w-full max-w-md bg-white/10 backdrop-blur-md border-white/20 text-white shadow-xl">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl">
          <Search className="w-5 h-5 text-amber-400" />
          Check My Numbers
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label>Select Lottery</Label>
          <Select
            onValueChange={(val) => {
              setSelectedLotteryId(val);
              setCheckResult(null);
            }}
          >
            <SelectTrigger className="bg-zinc-950/50 border-white/10 text-white">
              <SelectValue placeholder="Choose a lottery..." />
            </SelectTrigger>
            <SelectContent>
              {lotteries.map((l) => (
                <SelectItem key={l.id} value={l.id}>
                  {l.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label>Enter Your Numbers</Label>
          <div className="flex gap-2">
            {userNumbers.map((num, i) => (
              <Input
                key={i}
                value={num}
                onChange={(e) => handleNumberChange(i, e.target.value)}
                maxLength={2}
                className="w-10 h-10 p-0 text-center bg-zinc-950/50 border-white/10 text-white"
                placeholder="-"
              />
            ))}
            <div className="w-px bg-white/20 mx-1" />
            <Input
              value={bonusNumber}
              onChange={(e) => {
                if (e.target.value === "" || /^\d+$/.test(e.target.value)) {
                  setBonusNumber(e.target.value);
                }
              }}
              maxLength={2}
              className="w-10 h-10 p-0 text-center bg-amber-500/20 border-amber-500/50 text-amber-400 placeholder:text-amber-500/50"
              placeholder="B"
            />
          </div>
        </div>

        <Button
          onClick={handleCheck}
          className="w-full bg-gradient-to-r from-amber-500 to-yellow-600 hover:from-amber-600 hover:to-yellow-700 text-black font-bold"
        >
          Check Results
        </Button>

        {checkResult && (
          <div
            className={cn(
              "p-4 rounded-lg border flex items-center gap-3 animate-in fade-in slide-in-from-top-2",
              checkResult.matches > 0 || checkResult.bonusMatch
                ? "bg-green-500/20 border-green-500/30 text-green-200"
                : "bg-red-500/10 border-red-500/20 text-red-200",
            )}
          >
            {checkResult.matches > 0 || checkResult.bonusMatch ? (
              <Trophy className="w-6 h-6 text-green-400 shrink-0" />
            ) : (
              <XCircle className="w-6 h-6 text-red-400 shrink-0" />
            )}
            <div>
              <h4 className="font-bold">
                {checkResult.matches > 0 || checkResult.bonusMatch
                  ? "You Won!"
                  : "No Match"}
              </h4>
              <p className="text-sm opacity-90">
                Matches: {checkResult.matches} numbers
                {checkResult.bonusMatch && " + Bonus"}
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
