import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
// import { Navbar } from "@/components/navbar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Global Lotto - Win the World",
    template: "%s | Global Lotto",
  },
  description:
    "Track and subscribe to the biggest lotteries from across the globe (Powerball, Mega Millions, EuroMillions). Get instant notifications for results and jackpots.",
  keywords: [
    "Lottery",
    "Lotto",
    "Powerball",
    "Mega Millions",
    "Jackpot",
    "Results",
    "Global Lottery",
  ],
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://global-lotto.vercel.app/",
    siteName: "Global Lotto",
    images: [
      {
        url: "/og-image.jpg", // Placeholder
        width: 1200,
        height: 630,
        alt: "Global Lotto",
      },
    ],
  },
};

import { PwaInstallPrompt } from "@/components/pwa-install-prompt";
import { Toaster } from "@/components/ui/sonner";
import Script from "next/script";
import { Footer } from "@/components/footer";
import { CookieConsentComponent } from "@/components/cookie-consent";

import { Navbar } from "@/components/navbar";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#09090b" />
        <link rel="apple-touch-icon" href="/icon.png" />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-zinc-950 text-white min-h-screen flex flex-col`}
      >
        <Navbar />
        <main className="flex-grow">{children}</main>
        <Footer />
        <CookieConsentComponent />
        <PwaInstallPrompt />
        <Toaster />

        <Script
          id="register-sw"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{
            __html: `
              if ('serviceWorker' in navigator) {
                window.addEventListener('load', function() {
                  navigator.serviceWorker.register('/sw.js').then(
                    function(registration) {
                      console.log('Service Worker registration successful with scope: ', registration.scope);
                    },
                    function(err) {
                      console.log('Service Worker registration failed: ', err);
                    }
                  );
                });
              }
            `,
          }}
        />
      </body>
    </html>
  );
}
