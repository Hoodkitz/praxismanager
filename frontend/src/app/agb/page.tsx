import type { Metadata } from "next";
import LegalPage from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Allgemeine Geschäftsbedingungen – PraxisManager",
  robots: { index: false },
};

export default function Page() {
  return (
    <LegalPage title="Allgemeine Geschäftsbedingungen">
      <h2>1. Geltungsbereich</h2>
      <p>
        Diese AGB gelten für Verträge zwischen [PLATZHALTER: Anbieter] und seinen
        Kunden über die Nutzung von PraxisManager. [PLATZHALTER: Zielgruppe (Unternehmer / Verbraucher) festlegen]
      </p>
      <h2>2. Vertragsgegenstand und Leistungen</h2>
      <p>[PLATZHALTER: Leistungsbeschreibung, Funktionsumfang je Tarif]</p>
      <h2>3. Preise und Zahlung</h2>
      <p>
        Es gelten die zum Bestellzeitpunkt angezeigten Preise. [PLATZHALTER: Preise netto/brutto, MwSt., Abrechnungszeitraum]
        Die Zahlung erfolgt über Stripe.
      </p>
      <h2>4. Laufzeit und Kündigung</h2>
      <p>[PLATZHALTER: Mindestlaufzeit, Kündigungsfrist, Testphase falls angeboten]</p>
      <h2>5. Widerrufsrecht</h2>
      <p>[PLATZHALTER: Widerrufsbelehrung bei Verbrauchern bzw. Ausschluss bei reinen Unternehmerverträgen]</p>
      <h2>6. Haftung</h2>
      <p>[PLATZHALTER: Haftungsregelung, rechtlich prüfen lassen]</p>
      <h2>7. Haftungsausschluss / kein Rat</h2>
      <p>PraxisManager ist eine Verwaltungssoftware. Sie ersetzt keine ärztliche, therapeutische oder rechtliche Beratung und trifft keine medizinischen Entscheidungen. Verantwortlich für Behandlung, Dokumentation und Abrechnung bleibt allein der Praxisinhaber. Es wird keine Gewähr für Rechtskonformität (z. B. DSGVO, GOÄ/GOZ) übernommen.</p>
      <h2>8. Schlussbestimmungen</h2>
      <p>[PLATZHALTER: Anwendbares Recht, Gerichtsstand, salvatorische Klausel]</p>
    </LegalPage>
  );
}
