from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, patients, appointments, invoices, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PraxisManager API",
    description="Vertriebs- und Patientenmanagement für Arztpraxen",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(invoices.router)
app.include_router(dashboard.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
