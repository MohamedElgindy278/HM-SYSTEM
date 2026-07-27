from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import (
    user_router,
    insurance_provider_router,
    department_router,
    specialty_router,
    doctor_router,
    patient_router,
    insurance_policy_router,
    doctor_schedule_router,
    appointment_router,
    auth_router,
    dashboard_router,
    clinic_router,
    room_router,
    patient_queue_router,
)

app = FastAPI(
    title="HM-SYSTEM API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(dashboard_router.router)
app.include_router(user_router.router)
app.include_router(doctor_router.router)
app.include_router(doctor_schedule_router.router)
app.include_router(patient_router.router)
app.include_router(appointment_router.router)
app.include_router(department_router.router)
app.include_router(specialty_router.router)
app.include_router(insurance_provider_router.router)
app.include_router(insurance_policy_router.router)
app.include_router(clinic_router.router)
app.include_router(room_router.router)
app.include_router(patient_queue_router.router)
