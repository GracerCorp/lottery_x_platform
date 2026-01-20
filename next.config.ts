import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async rewrites() {
    return [
      {
        source: "/service-worker.js",
        destination: "/sw.js",
      },
    ];
  },
};

export default nextConfig;
