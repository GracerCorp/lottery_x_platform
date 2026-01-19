"use client";

import Link from "next/link";
import { Facebook, Twitter, Instagram } from "lucide-react";

export function Footer() {
  return (
    <footer className="w-full bg-zinc-950 border-t border-zinc-800 py-8 mt-auto">
      <div className="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-6">
        {/* Brand & Copyright */}
        <div className="flex flex-col items-center md:items-start gap-2">
          <Link href="/" className="text-xl font-bold text-white">
            Global Lottery Platform
          </Link>
          <p className="text-xs text-zinc-500 text-center md:text-left">
            © {new Date().getFullYear()} Global Lottery Platform. All rights
            reserved.
          </p>
        </div>

        {/* Navigation Links */}
        <nav className="flex flex-wrap justify-center gap-6 text-sm text-zinc-400">
          <Link href="/" className="hover:text-blue-400 transition-colors">
            Home
          </Link>
          <Link href="/terms" className="hover:text-blue-400 transition-colors">
            Terms of Service
          </Link>
          <Link
            href="/privacy"
            className="hover:text-blue-400 transition-colors"
          >
            Privacy Policy
          </Link>
        </nav>

        {/* Social Icons (Placeholder) */}
        <div className="flex items-center gap-4">
          <Link
            href="#"
            className="p-2 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white hover:border-zinc-600 transition-all"
          >
            <Facebook className="w-4 h-4" />
            <span className="sr-only">Facebook</span>
          </Link>
          <Link
            href="#"
            className="p-2 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white hover:border-zinc-600 transition-all"
          >
            <Twitter className="w-4 h-4" />
            <span className="sr-only">Twitter</span>
          </Link>
          <Link
            href="#"
            className="p-2 rounded-full bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white hover:border-zinc-600 transition-all"
          >
            <Instagram className="w-4 h-4" />
            <span className="sr-only">Instagram</span>
          </Link>
        </div>
      </div>
    </footer>
  );
}
