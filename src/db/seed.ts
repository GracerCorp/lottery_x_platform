import { db } from "./index";
import { lotteries, results } from "./schema";
import { calculateNextDraw, formatJackpot } from "@/lib/lottery";

async function seed() {
  console.log("🌱 Seeding database...");

  try {
    // Insert lotteries
    const lotteryData = [
      {
        name: "Powerball",
        slug: "powerball-usa",
        country: "USA",
        region: "North America",
        frequency: "Mon, Wed, Sat",
        logo: "/logos/powerball.png",
        description:
          "America's most popular lottery with record-breaking jackpots",
        officialLink: "https://www.powerball.com",
        isActive: true,
      },
      {
        name: "Mega Millions",
        slug: "mega-millions-usa",
        country: "USA",
        region: "North America",
        frequency: "Tue, Fri",
        logo: "/logos/megamillions.png",
        description: "One of the largest lottery games in the United States",
        officialLink: "https://www.megamillions.com",
        isActive: true,
      },
      {
        name: "EuroMillions",
        slug: "euromillions",
        country: "Europe",
        region: "Europe",
        frequency: "Tue, Fri",
        logo: "/logos/euromillions.png",
        description: "Europe's biggest lottery spanning 9 countries",
        officialLink: "https://www.euro-millions.com",
        isActive: true,
      },
      {
        name: "EuroJackpot",
        slug: "eurojackpot",
        country: "Europe",
        region: "Europe",
        frequency: "Tue, Fri",
        logo: "/logos/eurojackpot.png",
        description: "Pan-European lottery with massive prizes",
        officialLink: "https://www.eurojackpot.org",
        isActive: true,
      },
    ];

    console.log("📊 Inserting lotteries...");
    const insertedLotteries = await db
      .insert(lotteries)
      .values(lotteryData)
      .returning();
    console.log(`✅ Inserted ${insertedLotteries.length} lotteries`);

    // Insert sample results for each lottery
    console.log("🎲 Inserting results...");
    const resultData = insertedLotteries.flatMap((lottery, index) => {
      const baseJackpot = [245_000_000, 182_000_000, 164_000_000, 120_000_000][
        index
      ];
      const currency = lottery.country === "USA" ? "USD" : "EUR";

      return [
        {
          lotteryId: lottery.id,
          drawDate: calculateNextDraw(lottery.frequency!),
          numbers: JSON.stringify({
            main: [7, 21, 32, 41, 42],
            bonus: [16],
          }),
          jackpot: formatJackpot(baseJackpot, currency),
          currency: currency,
          winners: JSON.stringify([
            { tier: 1, prize: baseJackpot, count: 0 },
            { tier: 2, prize: 1_000_000, count: 3 },
          ]),
        },
        {
          lotteryId: lottery.id,
          drawDate: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
          numbers: JSON.stringify({
            main: [12, 23, 34, 45, 56],
            bonus: [8],
          }),
          jackpot: formatJackpot(baseJackpot * 0.8, currency),
          currency: currency,
          winners: JSON.stringify([
            { tier: 1, prize: baseJackpot * 0.8, count: 1 },
            { tier: 2, prize: 500_000, count: 5 },
          ]),
        },
      ];
    });

    await db.insert(results).values(resultData);
    console.log(`✅ Inserted ${resultData.length} results`);

    console.log("✨ Seeding completed successfully!");
  } catch (error) {
    console.error("❌ Error seeding database:", error);
    throw error;
  }

  process.exit(0);
}

seed();
