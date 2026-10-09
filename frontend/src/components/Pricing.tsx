"use client";

import { useState } from "react";
import { loadStripe } from "@stripe/stripe-js";

const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY || ""
);

const plans = [
  {
    name: "Basis",
    price: 49,
    description: "Für kleine Praxen und Einzeltherapeuten",
    features: [
      "Bis zu 500 Patienten",
      "Terminplanung",
      "E-Mail-Support",
      "1 Praxisstandort",
    ],
    priceId: process.env.NEXT_PUBLIC_STRIPE_PRICE_BASIC || "",
    popular: false,
  },
  {
    name: "Professional",
    price: 99,
    description: "Für wachsende Praxen und Teams",
    features: [
      "Unbegrenzte Patienten",
      "Terminplanung & Online-Buchung",
      "Rechnungen & GOÄ/GOZ",
      "Prioritäts-Support",
      "Bis zu 3 Praxisstandorte",
    ],
    priceId: process.env.NEXT_PUBLIC_STRIPE_PRICE_PROFESSIONAL || "",
    popular: true,
  },
  {
    name: "Enterprise",
    price: 149,
    description: "Für Kliniken und große Praxisgruppen",
    features: [
      "Alles aus Professional",
      "Unbegrenzte Praxisstandorte",
      "API-Zugang",
      "Persönlicher Ansprechpartner",
      "SLA mit 99,9% Verfügbarkeit",
    ],
    priceId: process.env.NEXT_PUBLIC_STRIPE_PRICE_ENTERPRISE || "",
    popular: false,
  },
];

export default function Pricing() {
  const [loading, setLoading] = useState<string | null>(null);

  const handleCheckout = async (priceId: string, planName: string) => {
    if (!priceId) {
      alert(
        `Stripe ist nicht konfiguriert. Bitte NEXT_PUBLIC_STRIPE_PRICE_${planName.toUpperCase()} in .env.local setzen.`
      );
      return;
    }

    setLoading(planName);
    try {
      const res = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ priceId }),
      });

      const data = await res.json();

      if (data.url) {
        window.location.href = data.url;
      } else {
        alert(data.error || "Fehler beim Erstellen der Checkout-Session");
      }
    } catch {
      alert("Netzwerkfehler. Bitte versuchen Sie es erneut.");
    } finally {
      setLoading(null);
    }
  };

  return (
    <section id="pricing" className="py-24 bg-gray-50">
      <div className="mx-auto max-w-7xl px-6">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
            Einfache, transparente Preise
          </h2>
          <p className="mt-4 text-lg leading-8 text-gray-600">
            Wählen Sie den Plan, der zu Ihrer Praxis passt. 14 Tage kostenlos testen, keine Kreditkarte erforderlich.
          </p>
        </div>

        <div className="mt-16 grid grid-cols-1 gap-8 lg:grid-cols-3">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl border p-8 ${
                plan.popular
                  ? "border-primary-600 bg-white shadow-xl shadow-primary-600/10 ring-1 ring-primary-600"
                  : "border-gray-200 bg-white"
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                  <span className="rounded-full bg-primary-600 px-4 py-1 text-xs font-semibold text-white">
                    Beliebteste Wahl
                  </span>
                </div>
              )}

              <div className="text-center">
                <h3 className="text-lg font-semibold text-gray-900">{plan.name}</h3>
                <p className="mt-1 text-sm text-gray-500">{plan.description}</p>
                <div className="mt-6">
                  <span className="text-4xl font-bold text-gray-900">{plan.price}€</span>
                  <span className="text-sm text-gray-500">/Monat</span>
                </div>
              </div>

              <ul className="mt-8 space-y-3">
                {plan.features.map((feature) => (
                  <li key={feature} className="flex items-start gap-3 text-sm text-gray-600">
                    <svg
                      className="h-5 w-5 flex-shrink-0 text-primary-500"
                      fill="none"
                      viewBox="0 0 24 24"
                      strokeWidth={2}
                      stroke="currentColor"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>

              <button
                onClick={() => handleCheckout(plan.priceId, plan.name)}
                disabled={loading !== null}
                className={`mt-8 w-full rounded-xl px-6 py-3 text-sm font-semibold transition-all ${
                  plan.popular
                    ? "bg-primary-600 text-white hover:bg-primary-700 shadow-lg shadow-primary-600/25"
                    : "border border-gray-300 text-gray-700 hover:border-gray-400 hover:bg-gray-50"
                } disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {loading === plan.name
                  ? "Wird geladen..."
                  : `Jetzt ${plan.name} testen`}
              </button>
            </div>
          ))}
        </div>

        <p className="mt-12 text-center text-sm text-gray-500">
          Alle Preise inkl. MwSt. Jederzeit kündbar. Testphase: 14 Tage kostenlos.
        </p>
      </div>
    </section>
  );
}
