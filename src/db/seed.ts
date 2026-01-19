import * as dotenv from "dotenv";
import { db } from "./index";
import { lotteries, results } from "./schema";
import { calculateNextDraw, formatJackpot } from "@/lib/lottery";

// Load environment variables from .env.local
dotenv.config({ path: ".env.local" });

async function seed() {
  console.log("🌱 Seeding database...");

  try {
    // Clear existing data
    console.log("🧹 Clearing existing data...");
    await db.delete(results);
    await db.delete(lotteries);

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
      // New Lotteries
      {
        name: "SuperEnalotto",
        slug: "superenalotto",
        country: "Italy",
        region: "Europe",
        frequency: "Tue, Thu, Fri, Sat",
        logo: "/logos/superenalotto.png",
        description:
          "Italy's favorite lottery with high odds but massive jackpots",
        officialLink: "https://www.superenalotto.com",
        isActive: true,
      },
      {
        name: "UK Lotto",
        slug: "uk-lotto",
        country: "UK",
        region: "Europe",
        frequency: "Wed, Sat",
        logo: "/logos/uk-lotto.png",
        description: "The National Lottery of the United Kingdom",
        officialLink: "https://www.national-lottery.co.uk",
        isActive: true,
      },
      {
        name: "El Gordo",
        slug: "el-gordo",
        country: "Spain",
        region: "Europe",
        frequency: "Sun",
        logo: "/logos/el-gordo.png",
        description: "Spain's Sunday lottery with a high chance of winning",
        officialLink: "https://www.elgordo.com",
        isActive: true,
      },
      {
        name: "La Primitiva",
        slug: "la-primitiva",
        country: "Spain",
        region: "Europe",
        frequency: "Mon, Thu, Sat",
        logo: "/logos/la-primitiva.png",
        description: "One of the oldest active lotteries in the world",
        officialLink: "https://www.loteriasyapuestas.es",
        isActive: true,
      },
      {
        name: "French Loto",
        slug: "french-loto",
        country: "France",
        region: "Europe",
        frequency: "Mon, Wed, Sat",
        logo: "/logos/french-loto.png",
        description: "France's flagship lottery game with rollover caps",
        officialLink: "https://www.fdj.fr",
        isActive: true,
      },
      {
        name: "Oz Lotto",
        slug: "oz-lotto",
        country: "Australia",
        region: "Oceania",
        frequency: "Tue",
        logo: "/logos/oz-lotto.png",
        description: "Australia's biggest jackpotting game",
        officialLink: "https://www.ozlotteries.com",
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
    // Helper to generate different winning numbers
    const generateNumbers = (count = 5, max = 50) => {
      const nums = new Set<number>();
      while (nums.size < count) nums.add(Math.floor(Math.random() * max) + 1);
      return Array.from(nums).sort((a, b) => a - b);
    };

    console.log("🎲 Inserting results...");
    const resultData = insertedLotteries.flatMap((lottery, index) => {
      // Base jackpots for the 10 lotteries
      const baseJackpots = [
        245_000_000,
        182_000_000, // US
        164_000_000,
        120_000_000, // Euro
        85_000_000, // SuperEnalotto (High)
        15_000_000, // UK Lotto
        8_000_000, // El Gordo
        25_000_000, // La Primitiva
        12_000_000, // French Loto
        30_000_000, // Oz Lotto
      ];

      const baseJackpot = baseJackpots[index] || 10_000_000;

      let currency = "EUR";
      if (lottery.country === "USA") currency = "USD";
      if (lottery.country === "UK") currency = "GBP";
      if (lottery.country === "Australia") currency = "AUD";

      return [
        {
          lotteryId: lottery.id,
          drawDate: calculateNextDraw(lottery.frequency!),
          numbers: JSON.stringify({
            main: generateNumbers(5, 50),
            bonus: generateNumbers(1, 12),
          }),
          jackpot: formatJackpot(baseJackpot, currency),
          currency: currency,
          winners: JSON.stringify([
            { tier: 1, prize: baseJackpot, count: 0 },
            { tier: 2, prize: 1_000_000, count: Math.floor(Math.random() * 5) },
          ]),
        },
        {
          lotteryId: lottery.id,
          drawDate: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
          numbers: JSON.stringify({
            main: generateNumbers(5, 50),
            bonus: generateNumbers(1, 12),
          }),
          jackpot: formatJackpot(baseJackpot * 0.8, currency),
          currency: currency,
          winners: JSON.stringify([
            { tier: 1, prize: baseJackpot * 0.8, count: 0 },
            { tier: 2, prize: 500_000, count: Math.floor(Math.random() * 10) },
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
