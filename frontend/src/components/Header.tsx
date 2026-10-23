import Link from "next/link";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-600 text-white font-bold text-sm">
            P
          </div>
          <span className="text-lg font-semibold text-gray-900">PraxisManager</span>
        </Link>
        <nav className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
            Features
          </a>
          <a href="#pricing" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
            Preise
          </a>
          <Link href="/impressum" className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors">
            Kontakt
          </Link>
        </nav>
        <div className="flex items-center gap-3">
          <Link
            href="#pricing"
            className="rounded-lg bg-primary-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-primary-700 transition-colors"
          >
            Preise
          </Link>
        </div>
      </div>
    </header>
  );
}
