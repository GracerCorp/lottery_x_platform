import { NextRequest, NextResponse } from "next/server";
import { db } from "@/db";
import { results, lotteries } from "@/db/schema";
import { eq, desc } from "drizzle-orm";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const lotteryId = searchParams.get("lotteryId");
    const limit = parseInt(searchParams.get("limit") || "10");

    let query = db
      .select({
        id: results.id,
        drawDate: results.drawDate,
        numbers: results.numbers,
        jackpot: results.jackpot,
        currency: results.currency,
        winners: results.winners,
        lottery: {
          id: lotteries.id,
          name: lotteries.name,
          slug: lotteries.slug,
          country: lotteries.country,
        },
      })
      .from(results)
      .leftJoin(lotteries, eq(results.lotteryId, lotteries.id))
      .orderBy(desc(results.drawDate))
      .limit(limit);

    // Apply lottery filter if provided
    if (lotteryId) {
      query = query.where(eq(results.lotteryId, lotteryId)) as typeof query;
    }

    const data = await query;

    return NextResponse.json(data);
  } catch (error) {
    console.error("Error fetching results:", error);
    return NextResponse.json(
      { error: "Failed to fetch results" },
      { status: 500 },
    );
  }
}
