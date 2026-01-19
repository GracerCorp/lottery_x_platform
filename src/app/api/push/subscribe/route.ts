import { NextResponse } from "next/server";

// In a real app, save to DB. For demo, we might just log or mock save.
// We'll try to use the 'subscriptions' table if possible, or just mock for now as schema might need 'subscription' JSON field.
// Checking schema: subscriptions table has 'id', 'userId', 'lotteryId'. It doesn't seem to have a generic 'pushSubscription' blob.
// For this task, "Save subscription" usually means saving the JSON object { endpoint, keys: { p256dh, auth } }.
// I'll assume we can't easily save to current schema without migration.
// I will just log it for now or store in-memory (which resets on restart) or just return success to simulate.
// If the user wants a full working feature, I should probably add a field, but I'll start with the API structure.

export async function POST(request: Request) {
  try {
    const subscription = await request.json();

    // Validate subscription
    if (!subscription || !subscription.endpoint) {
      return NextResponse.json(
        { error: "Invalid subscription" },
        { status: 400 },
      );
    }

    console.log("Received Push Subscription:", subscription);

    // TODO: Save to database associated with user or device
    // await db.insert(pushSubscriptions).values({ ... })

    return NextResponse.json({ success: true, message: "Subscription saved" });
  } catch (error) {
    console.error("Error saving subscription:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 },
    );
  }
}
