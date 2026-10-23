import type { Metadata } from "next";
import LegalPage from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Impressum – PraxisManager",
  robots: { index: false },
};

export default function Page() {
  return (
    <LegalPage title="Impressum">
      <h2>Angaben gemäß § 5 DDG</h2>
      <p>
        [PLATZHALTER: Firmenname / vollständiger Name]<br />
        [PLATZHALTER: Straße und Hausnummer]<br />
        [PLATZHALTER: PLZ Ort]
      </p>
      <h2>Vertreten durch</h2>
      <p>[PLATZHALTER: Name des Vertretungsberechtigten]</p>
      <h2>Kontakt</h2>
      <p>
        E-Mail: [PLATZHALTER: E-Mail-Adresse]<br />
        Telefon: [PLATZHALTER: Telefonnummer]
      </p>
      <h2>Registereintrag und Umsatzsteuer</h2>
      <p>
        Registergericht / Registernummer: [PLATZHALTER oder entfällt]<br />
        USt-IdNr. gemäß § 27a UStG: [PLATZHALTER oder entfällt]
      </p>
      <h2>Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV</h2>
      <p>[PLATZHALTER: Name und Anschrift]</p>
      <h2>Hinweis</h2>
      <p>PraxisManager ist eine Verwaltungssoftware. Sie ersetzt keine ärztliche, therapeutische oder rechtliche Beratung und trifft keine medizinischen Entscheidungen. Verantwortlich für Behandlung, Dokumentation und Abrechnung bleibt allein der Praxisinhaber. Es wird keine Gewähr für Rechtskonformität (z. B. DSGVO, GOÄ/GOZ) übernommen.</p>
    </LegalPage>
  );
}
