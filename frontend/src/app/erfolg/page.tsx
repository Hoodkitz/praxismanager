import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Erfolg – PraxisManager",
  description: "Ihr Abonnement wurde erfolgreich aktiviert.",
};

export default function ErfolgPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 px-6">
      <div className="w-full max-w-md rounded-2xl border border-gray-200 bg-white p-8 text-center shadow-sm">
        <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
          <svg
            className="h-8 w-8 text-green-600"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={2}
            stroke="currentColor"
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
          </svg>
        </div>
        <h1 className="mt-6 text-2xl font-bold text-gray-900">
          Zahlung erfolgreich!
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          Vielen Dank für Ihre Bestellung. Ihr Abonnement wurde aktiviert und
          Sie erhalten in Kürze eine Bestätigung per E-Mail.
        </p>
        <Link
          href="/"
          className="mt-6 inline-block rounded-xl bg-primary-600 px-6 py-3 text-sm font-semibold text-white hover:bg-primary-700 transition-colors"
        >
          Zurück zur Startseite
        </Link>
      </div>
    </div>
  );
}
