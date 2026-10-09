from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/appointments", tags=["appointments"])


@router.get("/", response_model=list[schemas.AppointmentResponse])
def list_appointments(
    skip: int = 0,
    limit: int = 100,
    from_date: datetime = None,
    to_date: datetime = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Appointment)
    if from_date:
        query = query.filter(models.Appointment.start_time >= from_date)
    if to_date:
        query = query.filter(models.Appointment.start_time <= to_date)
    return query.offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    if appointment.end_time <= appointment.start_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    db_appointment = models.Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.put("/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(appointment_id: int, appointment: schemas.AppointmentUpdate, db: Session = Depends(get_db)):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for key, value in appointment.model_dump(exclude_unset=True).items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
