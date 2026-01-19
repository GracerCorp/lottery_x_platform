"use client";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Checkbox } from "@/components/ui/checkbox";
import { Bell, Mail, Loader2 } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

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

export function SubscribeDialog({ lotteryName }: { lotteryName: string }) {
  const [email, setEmail] = useState("");
  const [notifyEmail, setNotifyEmail] = useState(true);
  const [notifyPush, setNotifyPush] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const handleSubscribe = async () => {
    setIsLoading(true);
    try {
      if (notifyPush) {
        if (!("serviceWorker" in navigator)) {
          toast.error("Push notifications are not supported in this browser.");
          return;
        }

        const registration = await navigator.serviceWorker.ready;
        const vapidPublicKey = process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY;

        if (!vapidPublicKey) {
          console.error("VAPID Public Key not found");
          toast.error("Configuration error: VAPID key missing.");
          return;
        }

        let sub = await registration.pushManager.getSubscription();

        if (!sub) {
          sub = await registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array(vapidPublicKey),
          });
        }

        const response = await fetch("/api/push/subscribe", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(sub),
        });

        if (!response.ok) {
          throw new Error("Failed to save push subscription");
        }
      }

      // Simulate email subscription saving or log it
      if (notifyEmail) {
        console.log(`Subscribing email ${email} to ${lotteryName}`);
        // In a real app, call API to save email subscription
      }

      toast.success(`Subscribed to ${lotteryName} successfully!`);
      setIsOpen(false);
      setEmail("");
    } catch (error) {
      console.error("Subscription failed:", error);
      toast.error("Failed to process subscription. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button className="w-full border border-zinc-700/50 gap-2 group">
          <Bell className="h-4 w-4 group-hover:shake" />
          Subscribe
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px] text-gray-900">
        <DialogHeader>
          <DialogTitle>Subscribe to {lotteryName}</DialogTitle>
          <DialogDescription>
            Get notified instantly when the results are out or the jackpot rolls
            over.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="email">Email address</Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="space-y-4 pt-2">
            <div className="flex items-center space-x-2 border p-3 rounded-md">
              <Checkbox
                id="notify-email"
                checked={notifyEmail}
                onCheckedChange={(c) => setNotifyEmail(!!c)}
              />
              <div className="grid gap-1.5 leading-none">
                <label
                  htmlFor="notify-email"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 flex items-center gap-2"
                >
                  <Mail className="h-4 w-4" />
                  Email Notifications
                </label>
              </div>
            </div>

            <div className="flex items-center space-x-2 border p-3 rounded-md">
              <Checkbox
                id="notify-push"
                checked={notifyPush}
                onCheckedChange={(c) => setNotifyPush(!!c)}
              />
              <div className="grid gap-1.5 leading-none">
                <label
                  htmlFor="notify-push"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70 flex items-center gap-2"
                >
                  <Bell className="h-4 w-4" />
                  Push Notifications
                </label>
              </div>
            </div>
          </div>
        </div>
        <DialogFooter>
          <Button
            onClick={handleSubscribe}
            disabled={!email || (!notifyEmail && !notifyPush) || isLoading}
          >
            {isLoading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
            Confirm Subscription
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
