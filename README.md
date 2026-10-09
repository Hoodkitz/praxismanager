# PraxisManager

Praxisverwaltung für Ärzte und Therapeuten – Patienten, Termine und Rechnungen zentral verwalten.

## Tech Stack

- **Frontend:** Next.js 16, React 19, Tailwind CSS 4, TypeScript
- **Backend:** FastAPI, Python 3.14
- **Zahlungen:** Stripe Checkout (Test-Modus)

## Projektstruktur

```
├── frontend/          # Next.js Landing Page + App
│   ├── src/app/       # Pages & API Routes
│   ├── src/components/# UI-Komponenten
│   └── src/app/api/checkout/  # Stripe Checkout Route
└── backend/           # FastAPI Backend
    ├── app/           # API Router, Models, Services
    └── tests/         # Pytest Tests
```

## Getting Started

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local  # Stripe Keys eintragen
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Stripe Konfiguration

1. Erstellen Sie ein Stripe-Konto unter [stripe.com](https://stripe.com)
2. Test-Keys unter [dashboard.stripe.com/test/apikeys](https://dashboard.stripe.com/test/apikeys) abrufen
3. Produkte/Preise unter [dashboard.stripe.com/test/products](https://dashboard.stripe.com/test/products) erstellen
4. Keys und Price-IDs in `frontend/.env.local` eintragen

## Features

- ✅ Landing Page mit Hero, Features, Pricing
- ✅ Stripe Checkout Integration (Test-Modus)
- ✅ Responsive Design (Tailwind CSS)
- ✅ DSGVO-konform
- ✅ FastAPI Backend mit Patienten-, Termin-, Rechnungs-APIs
