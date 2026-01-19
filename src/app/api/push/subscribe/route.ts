import { NextResponse } from "next/server";
import { db } from "@/db";
import { pushSubscriptions } from "@/db/schema";

export async function POST(request: Request) {
  try {
    const subscription = await request.json();

    // Validate subscription
    if (
      !subscription ||
      !subscription.endpoint ||
      !subscription.keys ||
      !subscription.keys.p256dh ||
      !subscription.keys.auth
    ) {
      return NextResponse.json(
        { error: "Invalid subscription" },
        { status: 400 },
      );
    }

    // Save to database
    // We try to insert and ignore logic isn't directly available in standard insert
    // But since endpoint is unique, we can check or perform upsert if supported or try/catch
    try {
      await db
        .insert(pushSubscriptions)
        .values({
          endpoint: subscription.endpoint,
          p256dh: subscription.keys.p256dh,
          auth: subscription.keys.auth,
          // userId: session?.user?.id // Can define if we extract session
        })
        .onConflictDoNothing();
    } catch (e) {
      console.warn("Subscription insert error (likely duplicate):", e);
    }

    return NextResponse.json({ success: true, message: "Subscription saved" });
  } catch (error) {
    console.error("Error saving subscription:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 },
    );
  }
}
