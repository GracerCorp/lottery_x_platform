"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Download, Share } from "lucide-react";

export function PwaInstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [isIOS, setIsIOS] = useState(false);
  const [isStandalone, setIsStandalone] = useState(false);

  useEffect(() => {
    // Check if running in standalone mode
    if (window.matchMedia("(display-mode: standalone)").matches) {
      setIsStandalone(true);
    }

    // Detect iOS
    const userAgent = window.navigator.userAgent.toLowerCase();
    setIsIOS(/iphone|ipad|ipod/.test(userAgent));

    // Capture install prompt event
    const handleBeforeInstallPrompt = (e: any) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };

    window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);

    return () => {
      window.removeEventListener(
        "beforeinstallprompt",
        handleBeforeInstallPrompt,
      );
    };
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;

    if (outcome === "accepted") {
      setDeferredPrompt(null);
    }
  };

  if (isStandalone) return null;

  return (
    <>
      {deferredPrompt && (
        <div className="fixed bottom-20 left-4 right-4 md:left-auto md:right-8 md:bottom-8 z-50 animate-in slide-in-from-bottom-5">
          <div className="bg-zinc-900 border border-zinc-700 rounded-xl p-4 shadow-2xl flex items-center justify-between gap-4 max-w-sm ml-auto">
            <div className="text-sm text-zinc-200">
              <strong>Install App</strong>
              <p className="text-xs text-zinc-400">
                Install for a better experience
              </p>
            </div>
            <Button
              onClick={handleInstallClick}
              size="sm"
              className="bg-blue-600 hover:bg-blue-500 text-white shrink-0"
            >
              <Download className="w-4 h-4 mr-2" />
              Install
            </Button>
          </div>
        </div>
      )}

      {/* iOS Information Toast/Banner - Simplistic version */}
      {isIOS && !isStandalone && (
        <div className="fixed bottom-20 left-4 right-4 md:left-auto md:right-8 md:bottom-8 z-50">
          <div className="bg-zinc-900/90 backdrop-blur border border-zinc-700 rounded-xl p-4 shadow-2xl max-w-sm ml-auto text-sm text-zinc-300">
            <div className="flex items-start gap-3">
              <Share className="w-5 h-5 text-blue-400 mt-0.5" />
              <div>
                <p className="font-medium text-white mb-1">Install on iOS</p>
                <p>
                  Tap the <strong>Share</strong> button and select{" "}
                  <strong>"Add to Home Screen"</strong>
                </p>
              </div>
              <button
                onClick={() => setIsIOS(false)}
                className="text-zinc-500 hover:text-white"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
