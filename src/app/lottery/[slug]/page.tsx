import { notFound } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Bell, Calendar, Trophy, History, Info } from "lucide-react";
import { CountdownTimer } from "@/components/countdown-timer";
import { PrizeBreakdown, WinnerTier } from "@/components/prize-breakdown";

interface LotteryNumbers {
  main: number[];
  bonus: number[];
}

async function getLottery(slug: string) {
  const { db } = await import("@/db");
  const { lotteries, results } = await import("@/db/schema");
  const { eq, desc } = await import("drizzle-orm");

  const lottery = await db.query.lotteries.findFirst({
    where: eq(lotteries.slug, slug),
  });

  if (!lottery) return null;

  const lotteryResults = await db.query.results.findMany({
    where: eq(results.lotteryId, lottery.id),
    orderBy: [desc(results.drawDate)],
    limit: 10,
  });

  return { lottery, results: lotteryResults };
}

export default async function LotteryDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const data = await getLottery(slug);

  if (!data) {
    notFound();
  }

  const { lottery, results: pastResults } = data;

  // Logic to find "next draw" and "latest result"
  // Assuming pastResults are sorted desc by date.
  // We want the most recent past draw for results display.
  // And we want the upcoming draw for the hero.
  // Since we don't have a separate "draws" table for future draws in this simple schema,
  // we might have to infer or just show the latest result + next estimated date.

  const latestResult = pastResults.find(
    (r) => new Date(r.drawDate) <= new Date(),
  );

  // For next draw, if we don't have a future record, we might need to calculate it or show placeholder
  // In a real app, we'd have a 'schedule' or 'future_draws' table.
  // Here we'll just check if there is a future result record seeded, or default to now + frequency.
  const nextDrawResult = pastResults.find(
    (r) => new Date(r.drawDate) > new Date(),
  ) || {
    // excessive fallback if no future data
    jackpot: "TBD",
    drawDate: new Date(Date.now() + 86400000 * 3), // +3 days
  };

  return (
    <div className="min-h-screen bg-zinc-950 pb-20">
      {/* Hero Section */}
      <div className="relative overflow-hidden border-b border-zinc-800 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/40 via-zinc-900/0 to-zinc-950 py-16 md:py-24">
        <div className="container mx-auto px-4 relative z-10">
          <div className="flex flex-col items-center text-center">
            {lottery.logo && (
              <div className="mb-6 h-24 w-24 md:h-32 md:w-32 bg-white/5 rounded-full p-4 border border-white/10 shadow-2xl backdrop-blur-sm flex items-center justify-center">
                <img
                  src={lottery.logo}
                  alt={lottery.name}
                  className="max-w-full max-h-full object-contain drop-shadow-lg"
                />
              </div>
            )}

            <h1 className="mb-4 text-4xl font-bold text-white md:text-6xl tracking-tight drop-shadow-md">
              {lottery.name}
            </h1>

            <div className="flex flex-wrap justify-center gap-3 text-zinc-300 mb-8">
              <span className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-zinc-800/80 border border-zinc-700 backdrop-blur-sm text-sm font-medium">
                {getCountryFlag(lottery.country)} {lottery.country}
              </span>
              <span className="flex items-center gap-2 px-4 py-1.5 rounded-full bg-zinc-800/80 border border-zinc-700 backdrop-blur-sm text-sm font-medium">
                <Calendar className="w-4 h-4 text-blue-400" />{" "}
                {lottery.frequency || "Weekly"}
              </span>
            </div>

            <div className="mb-8 p-8 bg-zinc-950/60 backdrop-blur-md rounded-3xl border border-zinc-800/60 shadow-2xl relative group">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-3xl blur-xl group-hover:blur-2xl transition-all duration-700 opacity-50"></div>
              <div className="relative">
                <div className="text-sm font-bold uppercase tracking-widest text-blue-400 mb-2">
                  Next Estimated Jackpot
                </div>
                <div className="text-6xl md:text-8xl font-black text-white mb-6 bg-gradient-to-br from-white via-zinc-200 to-zinc-500 bg-clip-text text-transparent">
                  {nextDrawResult?.jackpot || "Pending"}
                </div>
                <div className="flex justify-center">
                  <CountdownTimer
                    targetDate={
                      nextDrawResult?.drawDate instanceof Date
                        ? nextDrawResult.drawDate.toISOString()
                        : (nextDrawResult?.drawDate as unknown as string) ||
                          new Date().toISOString()
                    }
                  />
                </div>
              </div>
            </div>

            <Button
              size="lg"
              className="h-14 px-8 text-lg gap-3 bg-blue-600 hover:bg-blue-500 text-white rounded-full shadow-lg shadow-blue-900/20 active:scale-95 transition-transform"
            >
              <Bell className="w-5 h-5" />
              Get Results Alerts
            </Button>
          </div>
        </div>
      </div>

      {/* Content Grid */}
      <div className="container mx-auto mt-12 px-4">
        <div className="grid gap-12 lg:grid-cols-3">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-12">
            {/* Latest Winning Numbers */}
            <section>
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-yellow-500/10 rounded-lg">
                  <Trophy className="w-6 h-6 text-yellow-500" />
                </div>
                <div>
                  <h2 className="text-2xl font-bold text-white leading-none">
                    Latest Results
                  </h2>
                  <p className="text-zinc-500 text-sm mt-1">
                    Results for{" "}
                    {latestResult
                      ? new Date(latestResult.drawDate).toLocaleDateString(
                          undefined,
                          {
                            weekday: "long",
                            year: "numeric",
                            month: "long",
                            day: "numeric",
                          },
                        )
                      : "Recent Draw"}
                  </p>
                </div>
              </div>

              {latestResult ? (
                <div className="rounded-3xl border border-zinc-800 bg-zinc-900/50 p-8 md:p-10 relative overflow-hidden">
                  <div className="absolute top-0 right-0 p-4 opacity-10">
                    <Trophy className="w-48 h-48 text-white" />
                  </div>

                  <div className="flex flex-wrap gap-4 relative z-10 justify-center md:justify-start">
                    {(
                      latestResult.numbers as unknown as LotteryNumbers
                    ).main.map((num: number, idx: number) => (
                      <div
                        key={idx}
                        className="flex h-14 w-14 md:h-20 md:w-20 items-center justify-center rounded-full bg-zinc-800 text-2xl md:text-4xl font-bold text-white border-2 border-zinc-700 shadow-[inset_0_2px_4px_rgba(0,0,0,0.5)]"
                      >
                        {num}
                      </div>
                    ))}
                    {(
                      latestResult.numbers as unknown as LotteryNumbers
                    ).bonus.map((num: number, idx: number) => (
                      <div
                        key={idx}
                        className="flex h-14 w-14 md:h-20 md:w-20 items-center justify-center rounded-full bg-yellow-500 text-2xl md:text-4xl font-bold text-black border-4 border-yellow-600 shadow-lg glow-yellow"
                      >
                        {num}
                      </div>
                    ))}
                  </div>

                  {/* Prize Breakdown Component */}
                  <div className="mt-10">
                    <PrizeBreakdown
                      winners={latestResult.winners as unknown as WinnerTier[]}
                      currency={latestResult.currency || "USD"}
                    />
                  </div>
                </div>
              ) : (
                <div className="rounded-2xl border border-zinc-800 bg-zinc-900 p-8 text-center text-zinc-500">
                  No recent results available.
                </div>
              )}
            </section>

            {/* Past Results History */}
            <section>
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-zinc-800 rounded-lg">
                  <History className="w-6 h-6 text-zinc-400" />
                </div>
                <h2 className="text-2xl font-bold text-white">Draw History</h2>
              </div>

              <div className="space-y-4">
                {pastResults
                  .filter((r) => new Date(r.drawDate) <= new Date())
                  .slice(0, 10) // Limit to 10
                  .map((result) => (
                    <div
                      key={result.id}
                      className="group flex flex-col md:flex-row md:items-center justify-between gap-4 rounded-xl border border-zinc-800 bg-zinc-900/30 p-5 hover:bg-zinc-900/80 transition-all hover:border-zinc-700"
                    >
                      <div>
                        <div className="text-white font-bold text-lg">
                          {new Date(result.drawDate).toLocaleDateString(
                            undefined,
                            { dateStyle: "medium" },
                          )}
                        </div>
                        <div className="text-sm text-zinc-500 flex items-center gap-2">
                          <span>Jackpot:</span>
                          <span className="text-emerald-400 font-medium">
                            {result.jackpot}
                          </span>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        {(result.numbers as unknown as LotteryNumbers).main.map(
                          (n: number, i: number) => (
                            <span
                              key={i}
                              className="flex h-9 w-9 items-center justify-center rounded-full bg-zinc-800 text-sm font-bold text-zinc-300 border border-zinc-700"
                            >
                              {n}
                            </span>
                          ),
                        )}
                        {(
                          result.numbers as unknown as LotteryNumbers
                        ).bonus.map((n: number, i: number) => (
                          <span
                            key={i}
                            className="flex h-9 w-9 items-center justify-center rounded-full bg-yellow-500/20 text-sm font-bold text-yellow-500 border border-yellow-500/50"
                          >
                            {n}
                          </span>
                        ))}
                      </div>
                    </div>
                  ))}

                <Button
                  variant="outline"
                  className="w-full mt-4 border-zinc-800 text-zinc-400 hover:bg-zinc-900 hover:text-white"
                >
                  View Complete History
                </Button>
              </div>
            </section>
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            <div className="rounded-2xl border border-zinc-800 bg-zinc-900/80 p-6 sticky top-24 backdrop-blur-xl">
              <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                <Info className="w-5 h-5 text-blue-400" />
                About {lottery.name}
              </h3>

              <div className="prose prose-invert prose-sm text-zinc-400 mb-6 leading-relaxed">
                <p>
                  {lottery.description ||
                    `${lottery.name} is one of the most popular lotteries in ${lottery.country}. Drawings are held every ${lottery.frequency}.`}
                </p>
              </div>

              <dl className="space-y-4 text-sm border-t border-zinc-800 pt-6">
                <div className="flex justify-between items-center">
                  <dt className="text-zinc-500">Country</dt>
                  <dd className="text-white font-medium flex items-center gap-2">
                    {getCountryFlag(lottery.country)} {lottery.country}
                  </dd>
                </div>
                <div className="flex justify-between items-center">
                  <dt className="text-zinc-500">Region</dt>
                  <dd className="text-white font-medium">
                    {lottery.region || "Global"}
                  </dd>
                </div>
                <div className="flex justify-between items-center">
                  <dt className="text-zinc-500">Target Audience</dt>
                  <dd className="text-white font-medium">International</dd>
                </div>
                <div className="flex justify-between items-center">
                  <dt className="text-zinc-500">Rating</dt>
                  <dd className="text-amber-400 font-medium">★★★★★</dd>
                </div>
              </dl>

              {lottery.officialLink && (
                <Button
                  className="w-full mt-6 bg-zinc-800 hover:bg-zinc-700 text-white"
                  asChild
                >
                  <a
                    href={lottery.officialLink}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Visit Official Site
                  </a>
                </Button>
              )}
            </div>

            {/* Promo / Ad Space Placeholder */}
            {/* <div className="rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-600 p-6 text-center">
                <p className="font-bold text-white text-lg mb-2">Win Big Today!</p>
                <p className="text-indigo-100 text-sm mb-4">Don't miss your chance to change your life forever.</p>
                <Button variant="secondary" className="w-full">Play Now</Button>
            </div> */}
          </div>
        </div>
      </div>
    </div>
  );
}

function getCountryFlag(country: string): string {
  if (country === "USA") return "🇺🇸";
  if (country === "Europe") return "🇪🇺";
  if (country === "UK") return "🇬🇧";
  return "🌍";
}
