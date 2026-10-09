import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    staff = "staff"


class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"


class InvoiceStatus(str, enum.Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    overdue = "overdue"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.staff)
    created_at = Column(DateTime, default=datetime.utcnow)


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    date_of_birth = Column(String(10), nullable=True)  # YYYY-MM-DD
    insurance = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="patient", cascade="all, delete-orphan")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    title = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="appointments")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    invoice_number = Column(String(50), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    tax_rate = Column(Float, default=19.0)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.draft)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(String(10), nullable=True)  # YYYY-MM-DD

    patient = relationship("Patient", back_populates="invoices")
