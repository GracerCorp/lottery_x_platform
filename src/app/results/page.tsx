import { db } from "@/db";
import { lotteries, results } from "@/db/schema";
import { desc, eq } from "drizzle-orm";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { CalendarIcon, Trophy } from "lucide-react";
import Image from "next/image";

export const revalidate = 60; // Revalidate every minute

async function getLatestResults() {
  const activeLotteries = await db
    .select()
    .from(lotteries)
    .where(eq(lotteries.isActive, true));

  // Fetch the latest result for each lottery
  // We use distinctOn to get one result per lotteryId, ordered by date descending
  const latestResults = await db
    .selectDistinctOn([results.lotteryId])
    .from(results)
    .orderBy(results.lotteryId, desc(results.drawDate));

  return activeLotteries.map((lottery) => {
    const result = latestResults.find((r) => r.lotteryId === lottery.id);
    return {
      ...lottery,
      latestResult: result,
    };
  });
}

export default async function ResultsPage() {
  const lotteriesWithResults = await getLatestResults();

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col gap-2 mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Latest Results</h1>
        <p className="text-zinc-400">
          Check the winning numbers for your favorite lotteries.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {lotteriesWithResults.map((lottery) => (
          <Link
            key={lottery.id}
            href={`/lottery/${lottery.slug}`}
            className="block h-full transition-transform hover:scale-[1.02]"
          >
            <Card className="h-full bg-zinc-900/50 border-zinc-800 backdrop-blur-sm hover:border-zinc-700 transition-colors">
              <CardHeader className="pb-4">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 relative rounded-full bg-zinc-800 flex items-center justify-center overflow-hidden border border-zinc-700">
                      {lottery.logo ? (
                        <Image
                          src={lottery.logo}
                          alt={lottery.name}
                          fill
                          className="object-cover"
                        />
                      ) : (
                        <span className="text-xl font-bold text-zinc-500">
                          {lottery.name.substring(0, 1)}
                        </span>
                      )}
                    </div>
                    <div>
                      <CardTitle className="text-lg">{lottery.name}</CardTitle>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge
                          variant="outline"
                          className="text-xs border-zinc-700 text-zinc-400"
                        >
                          {lottery.country}
                        </Badge>
                      </div>
                    </div>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {lottery.latestResult ? (
                  <div className="space-y-4">
                    <div className="flex items-center gap-2 text-sm text-zinc-400">
                      <CalendarIcon className="w-4 h-4" />
                      <span>
                        {lottery.latestResult.drawDate.toLocaleDateString(
                          undefined,
                          {
                            weekday: "short",
                            year: "numeric",
                            month: "short",
                            day: "numeric",
                          },
                        )}
                      </span>
                    </div>

                    <div className="space-y-2">
                      <div className="flex flex-wrap gap-2">
                        {(
                          lottery.latestResult.numbers as { main: number[] }
                        ).main.map((num, idx) => (
                          <span
                            key={idx}
                            className="flex items-center justify-center w-8 h-8 rounded-full bg-zinc-800 text-white font-medium text-sm border border-zinc-700 shadow-sm"
                          >
                            {num}
                          </span>
                        ))}
                        {(
                          lottery.latestResult.numbers as { bonus: number[] }
                        ).bonus?.map((num, idx) => (
                          <span
                            key={`bonus-${idx}`}
                            className="flex items-center justify-center w-8 h-8 rounded-full bg-yellow-500/20 text-yellow-500 font-medium text-sm border border-yellow-500/50 shadow-sm"
                          >
                            {num}
                          </span>
                        ))}
                      </div>
                    </div>

                    {lottery.latestResult.jackpot && (
                      <div className="flex items-center gap-2 pt-2 border-t border-zinc-800 mt-4">
                        <Trophy className="w-4 h-4 text-emerald-500" />
                        <span className="text-sm font-medium text-emerald-500">
                          {lottery.latestResult.jackpot} Jackpot
                        </span>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="py-8 text-center text-zinc-500 text-sm italic">
                    No results available yet.
                  </div>
                )}
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
