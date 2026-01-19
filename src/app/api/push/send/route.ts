import { NextResponse } from "next/server";
import webpush from "web-push";

// Initialized lazily under handler

export async function POST(request: Request) {
  try {
    const { subscription, title, body } = await request.json();

    if (
      !process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY ||
      !process.env.VAPID_PRIVATE_KEY
    ) {
      console.warn("VAPID keys not set");
      return NextResponse.json(
        { error: "VAPID configuration missing" },
        { status: 500 },
      );
    }

    webpush.setVapidDetails(
      "mailto:test@example.com",
      process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY,
      process.env.VAPID_PRIVATE_KEY,
    );

    if (!subscription || !title) {
      return NextResponse.json(
        { error: "Missing required fields" },
        { status: 400 },
      );
    }

    const payload = JSON.stringify({
      title: title,
      body: body || "You have a new notification!",
    });

    await webpush.sendNotification(subscription, payload);

    return NextResponse.json({ success: true, message: "Notification sent" });
  } catch (error) {
    console.error("Error sending notification:", error);
    return NextResponse.json(
      { error: "Failed to send notification" },
      { status: 500 },
    );
  }
}
