from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import decode_access_token

router = APIRouter(prefix="/api/patients", tags=["patients"])


def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    # This is a simplified version - in production use OAuth2PasswordBearer
    from fastapi import Header
    auth_header = Header(None)
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_access_token(auth_header.split(" ")[1])
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == payload.get("user_id")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.get("/", response_model=list[schemas.PatientResponse])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Patient).offset(skip).limit(limit).all()


@router.post("/", response_model=schemas.PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.get("/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.put("/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(patient_id: int, patient: schemas.PatientUpdate, db: Session = Depends(get_db)):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in patient.model_dump(exclude_unset=True).items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(patient)
    db.commit()
