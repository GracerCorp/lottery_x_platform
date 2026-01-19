"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Trophy } from "lucide-react";

export interface WinnerTier {
  tier: string;
  match: string;
  prize: string;
  winners: number;
}

interface PrizeBreakdownProps {
  winners: WinnerTier[];
  currency?: string;
}

export function PrizeBreakdown({
  winners,
  currency = "USD",
}: PrizeBreakdownProps) {
  if (!winners || winners.length === 0) {
    return (
      <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-8 text-center text-zinc-500">
        <Trophy className="mx-auto h-12 w-12 text-zinc-700 mb-3 opacity-50" />
        <p>No prize breakdown available for this draw.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 overflow-hidden">
      <div className="p-4 border-b border-zinc-800 bg-zinc-900/50">
        <h3 className="font-bold text-white flex items-center gap-2">
          <Trophy className="w-4 h-4 text-yellow-500" />
          Prize Breakdown
        </h3>
      </div>
      <Table>
        <TableHeader className="bg-zinc-950/50">
          <TableRow className="border-zinc-800 hover:bg-transparent">
            <TableHead className="text-zinc-400">Match</TableHead>
            <TableHead className="text-zinc-400 text-right">Prize</TableHead>
            <TableHead className="text-zinc-400 text-right">Winners</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {winners.map((tier, index) => (
            <TableRow
              key={index}
              className="border-zinc-800 hover:bg-zinc-800/50 transition-colors"
            >
              <TableCell className="font-medium text-white">
                <div className="flex items-center gap-2">
                  {index === 0 && <span className="text-lg">👑</span>}
                  {tier.match}
                </div>
              </TableCell>
              <TableCell className="text-right text-emerald-400 font-mono">
                {tier.prize}
              </TableCell>
              <TableCell className="text-right text-zinc-300 font-mono">
                {(tier.winners || 0).toLocaleString()}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
