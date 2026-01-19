"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Ticket, Menu, Home, Trophy, Bell, Settings } from "lucide-react";
import { useState } from "react";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { label: "Home", href: "/", icon: Home },
    { label: "Results", href: "/results", icon: Trophy },
    { label: "My Tickets", href: "/tickets", icon: Ticket },
  ];

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-xl">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="h-8 w-8 bg-gradient-to-tr from-amber-600 to-yellow-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-900/20 group-hover:shadow-blue-900/40 transition-all">
            <Ticket className="w-5 h-5 text-white transform group-hover:-rotate-12 transition-transform" />
          </div>
          <span className="font-bold text-lg bg-gradient-to-r from-white to-zinc-400 bg-clip-text text-amber-500">
            Global Lotto
          </span>
        </Link>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-1">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-zinc-400 hover:text-white hover:bg-white/5 rounded-full transition-all"
            >
              <item.icon className="w-4 h-4" />
              {item.label}
            </Link>
          ))}
        </div>

        {/* Actions */}
        <div className="hidden md:flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            className="text-zinc-400 hover:text-white hover:bg-white/5 rounded-full"
          >
            <Bell className="w-5 h-5" />
          </Button>
          <Button className="bg-white text-black hover:bg-zinc-200 rounded-full px-6 font-semibold shadow-lg shadow-white/5">
            Log In
          </Button>
        </div>

        {/* Mobile Menu */}
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
          <SheetTrigger asChild>
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden text-zinc-400 hover:text-white"
            >
              <Menu className="w-6 h-6" />
            </Button>
          </SheetTrigger>
          <SheetContent
            side="right"
            className="bg-zinc-950 border-zinc-800 p-0"
          >
            <div className="flex flex-col h-full p-6">
              <div className="flex items-center gap-2 mb-8">
                <div className="h-8 w-8 bg-gradient-to-tr from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <Ticket className="w-5 h-5 text-white" />
                </div>
                <span className="font-bold text-lg text-white">
                  Global Lotto
                </span>
              </div>

              <div className="flex flex-col gap-2 space-y-1">
                {navItems.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setIsOpen(false)}
                    className="flex items-center gap-3 px-4 py-3 text-lg font-medium text-zinc-400 hover:text-white hover:bg-zinc-900 rounded-xl transition-all"
                  >
                    <item.icon className="w-5 h-5" />
                    {item.label}
                  </Link>
                ))}
              </div>

              <div className="mt-auto pt-6 border-t border-zinc-900 space-y-4">
                <Button className="w-full bg-blue-600 hover:bg-blue-500 text-white rounded-xl h-12 text-base">
                  Sign In
                </Button>
                <div className="flex justify-center gap-4 text-zinc-500">
                  <Link href="/terms" className="text-sm hover:text-zinc-300">
                    Terms
                  </Link>
                  <Link href="/privacy" className="text-sm hover:text-zinc-300">
                    Privacy
                  </Link>
                </div>
              </div>
            </div>
          </SheetContent>
        </Sheet>
      </div>
    </nav>
  );
}
