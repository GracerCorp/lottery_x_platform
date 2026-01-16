"use client"

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { Bell, Mail } from "lucide-react"
import { useState } from "react"

export function SubscribeDialog({ lotteryName }: { lotteryName: string }) {
  const [email, setEmail] = useState("")
  const [notifyEmail, setNotifyEmail] = useState(true)
  const [notifyPush, setNotifyPush] = useState(false)

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button className="w-full gap-2 group">
           <Bell className="h-4 w-4 group-hover:shake" />
           Subscribe
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Subscribe to {lotteryName}</DialogTitle>
          <DialogDescription>
            Get notified instantly when the results are out or the jackpot rolls over.
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
                <Checkbox id="notify-email" checked={notifyEmail} onCheckedChange={(c) => setNotifyEmail(!!c)} />
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
                <Checkbox id="notify-push" checked={notifyPush} onCheckedChange={(c) => setNotifyPush(!!c)} />
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
          <Button type="submit" disabled={!email || (!notifyEmail && !notifyPush)}>
              Confirm Subscription
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
