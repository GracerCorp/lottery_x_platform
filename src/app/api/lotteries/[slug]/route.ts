import { NextRequest, NextResponse } from "next/server";
import { db } from "@/db";
import { lotteries, results } from "@/db/schema";
import { eq, desc } from "drizzle-orm";

export async function GET(
  request: NextRequest,
  { params }: { params: { slug: string } },
) {
  try {
    const { slug } = params;

    // Fetch lottery by slug
    const [lottery] = await db
      .select()
      .from(lotteries)
      .where(eq(lotteries.slug, slug))
      .limit(1);

    if (!lottery) {
      return NextResponse.json({ error: "Lottery not found" }, { status: 404 });
    }

    // Fetch recent results for this lottery
    const recentResults = await db
      .select()
      .from(results)
      .where(eq(results.lotteryId, lottery.id))
      .orderBy(desc(results.drawDate))
      .limit(10);

    return NextResponse.json({
      lottery,
      results: recentResults,
    });
  } catch (error) {
    console.error("Error fetching lottery:", error);
    return NextResponse.json(
      { error: "Failed to fetch lottery" },
      { status: 500 },
    );
  }
}
