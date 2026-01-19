import { NextResponse } from "next/server";
import webpush from "web-push";

webpush.setVapidDetails(
  "mailto:test@example.com",
  process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY!,
  process.env.VAPID_PRIVATE_KEY!,
);

export async function POST(request: Request) {
  try {
    const { subscription, title, body } = await request.json();

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
