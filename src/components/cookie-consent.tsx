"use client";

import { useEffect } from "react";
import * as CookieConsent from "vanilla-cookieconsent";
import { config } from "@/lib/cookie-config";

export function CookieConsentComponent() {
  useEffect(() => {
    CookieConsent.run(config);
  }, []);

  return null;
}
