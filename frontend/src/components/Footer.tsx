import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-white">
      <div className="mx-auto max-w-7xl px-6 py-12">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
          <div>
            <Link href="/" className="flex items-center gap-2">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-600 text-white font-bold text-sm">
                P
              </div>
              <span className="text-lg font-semibold text-gray-900">PraxisManager</span>
            </Link>
            <p className="mt-4 text-sm text-gray-500">
              Die moderne Praxisverwaltung für Ärzte und Therapeuten.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-gray-900">Produkt</h4>
            <ul className="mt-4 space-y-2">
              <li><a href="#features" className="text-sm text-gray-500 hover:text-gray-700">Features</a></li>
              <li><a href="#pricing" className="text-sm text-gray-500 hover:text-gray-700">Preise</a></li>
              <li><a href="#" className="text-sm text-gray-500 hover:text-gray-700">Changelog</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-gray-900">Rechtliches</h4>
            <ul className="mt-4 space-y-2">
              <li><a href="#" className="text-sm text-gray-500 hover:text-gray-700">Impressum</a></li>
              <li><a href="#" className="text-sm text-gray-500 hover:text-gray-700">Datenschutz</a></li>
              <li><a href="#" className="text-sm text-gray-500 hover:text-gray-700">AGB</a></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-gray-900">Support</h4>
            <ul className="mt-4 space-y-2">
              <li><a href="#" className="text-sm text-gray-500 hover:text-gray-700">Hilfe-Center</a></li>
              <li><a href="#" className="text-sm text-gray-500 hover:text-gray-700">Kontakt</a></li>
              <li><a href="#" className="text-sm text-gray-500 hover:text-gray-700">Status</a></li>
            </ul>
          </div>
        </div>

        <div className="mt-12 border-t border-gray-200 pt-8 text-center text-sm text-gray-500">
          © 2026 PraxisManager. Alle Rechte vorbehalten.
        </div>
      </div>
    </footer>
  );
}
