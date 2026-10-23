import Link from "next/link";

export default function LegalPage({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <main className="mx-auto max-w-3xl px-6 py-16 text-gray-800">
      <Link href="/" className="text-sm text-blue-600 hover:underline">
        &larr; Zurück zur Startseite
      </Link>
      <h1 className="mt-6 text-3xl font-bold">{title}</h1>
      <p className="mt-4 rounded-lg border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">
        Entwurf: Alle mit [PLATZHALTER] markierten Angaben müssen vor Veröffentlichung
        durch die tatsächlichen Daten ersetzt und der Text rechtlich geprüft werden.
        Dieser Text ist keine Rechtsberatung.
      </p>
      <div className="mt-8 space-y-4 leading-7 [&_h2]:mt-8 [&_h2]:text-xl [&_h2]:font-semibold">
        {children}
      </div>
    </main>
  );
}
