import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

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
  description: "Track and subscribe to the biggest lotteries from across the globe (Powerball, Mega Millions, EuroMillions). Get instant notifications for results and jackpots.",
  keywords: ["Lottery", "Lotto", "Powerball", "Mega Millions", "Jackpot", "Results", "Global Lottery"],
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
           alt: "Global Lotto"
       }
    ]
  }
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
