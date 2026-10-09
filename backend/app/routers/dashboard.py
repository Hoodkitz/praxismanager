from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_patients = db.query(models.Patient).count()
    total_appointments = db.query(models.Appointment).count()
    upcoming_appointments = (
        db.query(models.Appointment)
        .filter(models.Appointment.start_time >= datetime.utcnow())
        .count()
    )
    total_invoices = db.query(models.Invoice).count()
    open_invoices = (
        db.query(models.Invoice)
        .filter(models.Invoice.status.in_(["draft", "sent", "overdue"]))
        .count()
    )
    revenue = (
        db.query(models.Invoice)
        .filter(models.Invoice.status == "paid")
        .with_entities(models.Invoice.amount)
        .all()
    )
    total_revenue = sum(r[0] for r in revenue) if revenue else 0.0

    return schemas.DashboardStats(
        total_patients=total_patients,
        total_appointments=total_appointments,
        upcoming_appointments=upcoming_appointments,
        total_invoices=total_invoices,
        open_invoices=open_invoices,
        revenue=total_revenue,
    )
