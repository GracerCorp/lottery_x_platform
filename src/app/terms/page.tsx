import React from "react";

export default function TermsPage() {
  return (
    <div className="container mx-auto max-w-4xl py-12 px-4 text-zinc-300">
      <h1 className="text-3xl font-bold text-white mb-6">Terms of Service</h1>
      <p className="mb-4">Last updated: {new Date().toLocaleDateString()}</p>

      <section className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold text-white">
          1. Acceptance of Terms
        </h2>
        <p>
          By accessing and using Global Lotto (the "Service"), you accept and
          agree to be bound by the terms and provision of this agreement. In
          addition, when using these particular services, you shall be subject
          to any posted guidelines or rules applicable to such services.
        </p>
      </section>

      <section className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold text-white">
          2. Disclaimer of Warranties
        </h2>
        <p>
          The services and all information, products, and other content included
          in or accessible from this website are provided either by "as is" or
          "as available" basis and are subject to change at any time without
          notice to you. We verify the lottery results to the best of our
          ability but do not guarantee 100% accuracy. Please verify with
          official sources.
        </p>
      </section>

      <section className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold text-white">
          3. Intellectual Property
        </h2>
        <p>
          The content, organization, graphics, design, compilation, magnetic
          translation, digital conversion and other matters related to the Site
          are protected under applicable copyrights, trademarks and other
          proprietary (including but not limited to intellectual property)
          rights.
        </p>
      </section>

      <section className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold text-white">
          4. Limitation of Liability
        </h2>
        <p>
          In no event will we be liable for any direct, indirect, incidental,
          special, consequential or punitive damages resulting from your access
          to or use of, or inability to access or use, the website or any
          content on the website.
        </p>
      </section>

      <section className="space-y-4 mb-8">
        <h2 className="text-xl font-semibold text-white">
          5. Changes to Terms
        </h2>
        <p>
          We reserve the right to modify these terms from time to time at our
          sole discretion. Therefore, you should review this page periodically.
          Your continued use of the Website after those changes constitute your
          agreement to the new Terms.
        </p>
      </section>
    </div>
  );
}
