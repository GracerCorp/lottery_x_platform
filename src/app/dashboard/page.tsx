import { auth } from "@/auth";
import { redirect } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Bell, CreditCard, User, LogOut } from "lucide-react";
import { signOut } from "@/auth";
import Link from "next/link";

export default async function DashboardPage() {
  const session = await auth();

  if (!session?.user) {
    redirect("/login");
  }

  return (
    <div className="min-h-screen bg-zinc-950 p-6 md:p-12">
      <div className="mx-auto max-w-6xl space-y-8">
        {/* Header */}
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">Dashboard</h1>
            <p className="text-zinc-400">
              Manage your subscriptions and settings.
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-zinc-400">
              Signed in as{" "}
              <span className="text-white font-medium">
                {session.user.email}
              </span>
            </span>
            <form
              action={async () => {
                "use server";
                await signOut({ redirectTo: "/" });
              }}
            >
              <Button
                variant="outline"
                size="sm"
                className="gap-2 border-zinc-700 bg-zinc-900 hover:bg-zinc-800 text-white"
              >
                <LogOut className="h-4 w-4" />
                Sign Out
              </Button>
            </form>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid gap-6 md:grid-cols-3">
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
            <div className="flex items-center gap-4">
              <div className="rounded-lg bg-blue-500/10 p-3 text-blue-500">
                <Bell className="h-6 w-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-zinc-400">
                  Active Alerts
                </p>
                <p className="text-2xl font-bold text-white">0</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
            <div className="flex items-center gap-4">
              <div className="rounded-lg bg-green-500/10 p-3 text-green-500">
                <CreditCard className="h-6 w-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-zinc-400">
                  Subscriptions
                </p>
                <p className="text-2xl font-bold text-white">0</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-zinc-800 bg-zinc-900/50 p-6">
            <div className="flex items-center gap-4">
              <div className="rounded-lg bg-purple-500/10 p-3 text-purple-500">
                <User className="h-6 w-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-zinc-400">
                  Account Status
                </p>
                <p className="text-lg font-bold text-white capitalize">
                  {(session.user as { role?: string }).role || "User"}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Subscriptions Section (Placeholder for V2) */}
        <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-6">
          <h2 className="text-xl font-bold text-white mb-4">
            My Subscriptions
          </h2>
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <div className="rounded-full bg-zinc-800 p-4 mb-4">
              <Bell className="h-8 w-8 text-zinc-500" />
            </div>
            <h3 className="text-lg font-medium text-white">
              No active subscriptions
            </h3>
            <p className="text-zinc-400 max-w-sm mt-2">
              Browse lotteries and click the bell icon to get notified about
              jackpots and results.
            </p>
            <Button
              className="mt-6 bg-blue-600 hover:bg-blue-500 text-white"
              asChild
            >
              <Link href="/">Browse Lotteries</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
