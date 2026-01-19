import { NextRequest, NextResponse } from "next/server";
import { db } from "@/db";
import { lotteries, results } from "@/db/schema";
import { eq, desc } from "drizzle-orm";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const country = searchParams.get("country");
    const limit = parseInt(searchParams.get("limit") || "10");

    // Build base query
    const baseQuery = db
      .select({
        id: lotteries.id,
        name: lotteries.name,
        slug: lotteries.slug,
        country: lotteries.country,
        region: lotteries.region,
        frequency: lotteries.frequency,
        logo: lotteries.logo,
        description: lotteries.description,
        officialLink: lotteries.officialLink,
      })
      .from(lotteries)
      .where(eq(lotteries.isActive, true))
      .limit(limit);

    // Execute query (country filter can be added in v2)
    const data = await baseQuery;

    // Fetch latest result for each lottery to get current jackpot
    const lotteriesWithJackpots = await Promise.all(
      data.map(async (lottery) => {
        const [latestResult] = await db
          .select({
            jackpot: results.jackpot,
            drawDate: results.drawDate,
            currency: results.currency,
          })
          .from(results)
          .where(eq(results.lotteryId, lottery.id))
          .orderBy(desc(results.drawDate))
          .limit(1);

        return {
          ...lottery,
          jackpot: latestResult?.jackpot || "$0",
          nextDraw:
            latestResult?.drawDate?.toISOString() || new Date().toISOString(),
          currency: latestResult?.currency || "USD",
        };
      }),
    );

    return NextResponse.json(lotteriesWithJackpots);
  } catch (error) {
    console.error("Error fetching lotteries:", error);
    return NextResponse.json(
      { error: "Failed to fetch lotteries" },
      { status: 500 },
    );
  }
}
