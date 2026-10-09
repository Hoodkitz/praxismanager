from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/invoices", tags=["invoices"])


def generate_invoice_number(db: Session) -> str:
    count = db.query(models.Invoice).count()
    return f"INV-{datetime.now().year}-{count + 1:04d}"


@router.get("/", response_model=list[schemas.InvoiceResponse])
def list_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Invoice).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    db_invoice = models.Invoice(
        **invoice.model_dump(),
        invoice_number=generate_invoice_number(db),
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


@router.get("/{invoice_id}", response_model=schemas.InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.put("/{invoice_id}", response_model=schemas.InvoiceResponse)
def update_invoice(invoice_id: int, invoice: schemas.InvoiceUpdate, db: Session = Depends(get_db)):
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    for key, value in invoice.model_dump(exclude_unset=True).items():
        setattr(db_invoice, key, value)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    db.delete(invoice)
    db.commit()
