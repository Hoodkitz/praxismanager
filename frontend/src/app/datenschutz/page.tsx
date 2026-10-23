import type { Metadata } from "next";
import LegalPage from "@/components/LegalPage";

export const metadata: Metadata = {
  title: "Datenschutzerklärung – PraxisManager",
  robots: { index: false },
};

export default function Page() {
  return (
    <LegalPage title="Datenschutzerklärung">
      <h2>1. Verantwortlicher</h2>
      <p>
        [PLATZHALTER: Name und Anschrift des Verantwortlichen, E-Mail]
      </p>
      <h2>2. Hosting</h2>
      <p>
        Diese Website wird bei [PLATZHALTER: Hosting-Anbieter, z. B. Vercel] gehostet.
        Beim Aufruf werden technisch notwendige Verbindungsdaten (z. B. IP-Adresse,
        Zeitpunkt, aufgerufene Seite) in Server-Logfiles verarbeitet.
        Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO. [PLATZHALTER: Speicherdauer, Auftragsverarbeitungsvertrag prüfen]
      </p>
      <h2>3. Zahlungsabwicklung über Stripe</h2>
      <p>
        Für Zahlungen nutzen wir Stripe Checkout (Stripe Payments Europe, Ltd., Irland, ggf.
        Stripe, Inc., USA). Bei Kauf werden Sie auf Stripe weitergeleitet; dort werden
        Zahlungs- und Kontaktdaten verarbeitet. Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO.
        Informationen: stripe.com/de/privacy. [PLATZHALTER: Drittlandübermittlung / Garantien prüfen]
      </p>
      <h2>4. Kontaktaufnahme</h2>
      <p>
        Bei Kontakt per E-Mail verarbeiten wir Ihre Angaben zur Bearbeitung der Anfrage.
        [PLATZHALTER: Speicherdauer]
      </p>
      <h2>5. Ihre Rechte</h2>
      <p>
        Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der
        Verarbeitung, Datenübertragbarkeit und Widerspruch sowie das Recht auf
        Beschwerde bei einer Aufsichtsbehörde.
      </p>
      <h2>6. Cookies / Tracking</h2>
      <p>
        [PLATZHALTER: Angeben, ob Cookies, Analyse- oder Tracking-Tools eingesetzt werden.
        Derzeit setzt diese Seite selbst keine Tracking-Dienste ein.]
      </p>
      <h2>Hinweis</h2>
      <p>PraxisManager ist eine Verwaltungssoftware. Sie ersetzt keine ärztliche, therapeutische oder rechtliche Beratung und trifft keine medizinischen Entscheidungen. Verantwortlich für Behandlung, Dokumentation und Abrechnung bleibt allein der Praxisinhaber. Es wird keine Gewähr für Rechtskonformität (z. B. DSGVO, GOÄ/GOZ) übernommen.</p>
    </LegalPage>
  );
}
