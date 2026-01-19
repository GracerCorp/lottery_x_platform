import React from "react";

export default function PrivacyPage() {
  return (
    <div className="container mx-auto max-w-4xl py-12 px-4 text-zinc-300">
      <h1 className="text-3xl font-bold text-white mb-6">Privacy Policy</h1>
      <p className="mb-4">Last updated: {new Date().toLocaleDateString()}</p>

      <section className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold text-white">1. Introduction</h2>
        <p>
          Welcome to Global Lotto ("we," "our," or "us"). We are committed to
          protecting your privacy and ensuring you have a positive experience on
          our website. This Privacy Policy explains how we collect, use, and
          share your personal information when you visit our site.
        </p>
      </section>

      <section className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold text-white">
          2. Information We Collect
        </h2>
        <ul className="list-disc pl-5 space-y-2">
          <li>
            <strong>Personal Information:</strong> We may collect personal
            information such as your name and email address when you voluntarily
            subscribe to our newsletters or notifications.
          </li>
          <li>
            <strong>Usage Data:</strong> We automatically collect information
            about how you interact with our website, including your IP address,
            browser type, pages visited, and time spent on the site.
          </li>
          <li>
            <strong>Cookies:</strong> We use cookies to enhance your browsing
            experience and analyze site traffic. You can manage your cookie
            preferences through our settings.
          </li>
        </ul>
      </section>

      <section className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold text-white">
          3. How We Use Your Information
        </h2>
        <p>We use the collected information for the following purposes:</p>
        <ul className="list-disc pl-5 space-y-2">
          <li>To provide and maintain our services.</li>
          <li>
            To send you updates, newsletters, and promotional materials (if
            subscribed).
          </li>
          <li>
            To analyze usage patterns and improve our website functionality.
          </li>
          <li>To comply with legal obligations.</li>
        </ul>
      </section>

      <section className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold text-white">
          4. Data Protection (GDPR & PDPA)
        </h2>
        <p>
          We respect your rights under the General Data Protection Regulation
          (GDPR) and the Personal Data Protection Act (PDPA). You have the right
          to access, correct, delete, or restrict the processing of your
          personal data. To exercise these rights, please contact us.
        </p>
      </section>

      <section className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold text-white">5. Contact Us</h2>
        <p>
          If you have any questions about this Privacy Policy, please contact us
          at support@globallotto.com.
        </p>
      </section>
    </div>
  );
}
