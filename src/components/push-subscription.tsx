"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Bell, BellOff, Loader2 } from "lucide-react";
import { toast } from "sonner"; // Assuming sonner is installed, or we can use standard alert/console

function urlBase64ToUint8Array(base64String: string) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, "+")
    .replace(/_/g, "/");

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

export function PushSubscription() {
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [subscription, setSubscription] = useState<PushSubscription | null>(
    null,
  );

  useEffect(() => {
    if ("serviceWorker" in navigator && "PushManager" in window) {
      navigator.serviceWorker.ready.then((registration) => {
        registration.pushManager.getSubscription().then((sub) => {
          if (sub) {
            setIsSubscribed(true);
            setSubscription(sub);
          }
        });
      });
    }
  }, []);

  const subscribeUser = async () => {
    setIsLoading(true);
    try {
      const registration = await navigator.serviceWorker.ready;
      const vapidPublicKey = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY;

      if (!vapidPublicKey) {
        throw new Error("VAPID Public Key not found");
      }

      const sub = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(vapidPublicKey),
      });

      // Save subscription to backend
      const response = await fetch("/api/push/subscribe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(sub),
      });

      if (response.ok) {
        setSubscription(sub);
        setIsSubscribed(true);
        toast.success("Notifications enabled!");

        // Optional: Send a test notification immediately
        await fetch("/api/push/send", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            subscription: sub,
            title: "Welcome!",
            body: "You've successfully subscribed to lottery alerts.",
          }),
        });
      } else {
        toast.error("Failed to save subscription");
      }
    } catch (error) {
      console.error("Failed to subscribe:", error);
      toast.error(
        "Failed to enable notifications. Please check your browser settings.",
      );
    } finally {
      setIsLoading(false);
    }
  };

  const unsubscribeUser = async () => {
    setIsLoading(true);
    try {
      if (subscription) {
        await subscription.unsubscribe();
        setSubscription(null);
        setIsSubscribed(false);
        toast.success("Notifications disabled.");
      }
    } catch (error) {
      console.error("Error unsubscribing", error);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isSubscribed) {
    return (
      <Button
        variant="outline"
        onClick={subscribeUser}
        disabled={isLoading}
        className="gap-2 border-zinc-700 bg-zinc-800/50 hover:bg-zinc-800 text-zinc-300"
      >
        {isLoading ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : (
          <Bell className="w-4 h-4" />
        )}
        Enable Alerts
      </Button>
    );
  }

  return (
    <Button
      variant="outline"
      onClick={unsubscribeUser}
      disabled={isLoading}
      className="gap-2 border-red-900/30 bg-red-900/10 hover:bg-red-900/20 text-red-400"
    >
      {isLoading ? (
        <Loader2 className="w-4 h-4 animate-spin" />
      ) : (
        <BellOff className="w-4 h-4" />
      )}
      Disable Alerts
    </Button>
  );
}
