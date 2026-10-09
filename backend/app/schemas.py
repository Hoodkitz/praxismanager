from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# --- Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

    class Config:
        from_attributes = True


# --- Patient ---
class PatientCreate(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    insurance: Optional[str] = None
    notes: Optional[str] = None


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    insurance: Optional[str] = None
    notes: Optional[str] = None


class PatientResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    insurance: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Appointment ---
class AppointmentCreate(BaseModel):
    patient_id: int
    title: str = Field(min_length=1)
    start_time: datetime
    end_time: datetime
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    title: str
    start_time: datetime
    end_time: datetime
    status: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# --- Invoice ---
class InvoiceCreate(BaseModel):
    patient_id: int
    amount: float = Field(gt=0)
    tax_rate: float = 19.0
    description: Optional[str] = None
    due_date: Optional[str] = None


class InvoiceUpdate(BaseModel):
    status: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None


class InvoiceResponse(BaseModel):
    id: int
    patient_id: int
    invoice_number: str
    amount: float
    tax_rate: float
    status: str
    description: Optional[str] = None
    created_at: datetime
    due_date: Optional[str] = None

    class Config:
        from_attributes = True


# --- Dashboard ---
class DashboardStats(BaseModel):
    total_patients: int
    total_appointments: int
    upcoming_appointments: int
    total_invoices: int
    open_invoices: int
    revenue: float
