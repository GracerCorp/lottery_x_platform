import { model } from "./gemini";

interface ParsedResult {
    drawDate: string;
    numbers: number[];
    bonusText?: string;
    jackpot?: string;
}

export async function parseLotteryResult(rawText: string, lotteryName: string): Promise<ParsedResult | null> {
    try {
        const prompt = `
        You are a lottery result parser. Extract the draw date, winning numbers, and jackpot from the following text for the lottery "${lotteryName}".
        Return ONLY valid JSON with this structure:
        {
            "drawDate": "YYYY-MM-DD",
            "numbers": [1, 2, 3],
            "bonusText": "Bonus Ball 5",
            "jackpot": "$10 Million"
        }
        
        Text to parse:
        ${rawText}
        `;

        const result = await model.generateContent(prompt);
        const response = result.response;
        const text = response.text();
        
        // Cleanup markdown code blocks if present
        const jsonStr = text.replace(/```json/g, '').replace(/```/g, '').trim();
        return JSON.parse(jsonStr);
    } catch (error) {
        console.error("Error parsing lottery result with Gemini:", error);
        return null;
    }
}
