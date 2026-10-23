import { NextRequest, NextResponse } from "next/server";
import Stripe from "stripe";

function getStripe() {
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) {
    throw new Error("STRIPE_SECRET_KEY ist nicht konfiguriert");
  }
  return new Stripe(key);
}

function getAllowedPriceIds(): Set<string> {
  return new Set(
    (process.env.STRIPE_ALLOWED_PRICE_IDS || "")
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean)
  );
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { priceId } = body;

    if (typeof priceId !== "string" || !priceId) {
      return NextResponse.json(
        { error: "priceId ist erforderlich" },
        { status: 400 }
      );
    }

    const allowed = getAllowedPriceIds();
    if (allowed.size === 0) {
      console.error("STRIPE_ALLOWED_PRICE_IDS ist nicht konfiguriert");
      return NextResponse.json(
        { error: "Checkout ist nicht konfiguriert" },
        { status: 503 }
      );
    }
    if (!allowed.has(priceId)) {
      return NextResponse.json({ error: "Ungültige priceId" }, { status: 400 });
    }

    const stripe = getStripe();
    const session = await stripe.checkout.sessions.create({
      mode: "subscription",
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      success_url: `${req.nextUrl.origin}/erfolg?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.nextUrl.origin}/#pricing`,
      locale: "de",
      metadata: {
        source: "praxismanager-landing",
      },
    });

    return NextResponse.json({ url: session.url });
  } catch (error) {
    console.error("Stripe Checkout Error:", error);
    return NextResponse.json(
      { error: "Fehler beim Erstellen der Checkout-Session" },
      { status: 500 }
    );
  }
}
