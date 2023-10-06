#!/usr/bin/env python3

from app import app
from models import db  # models go here
from faker import Faker
from random import randint, choice, choices
from models import Doctor, Patient, Appointment


fake = Faker()

if __name__ == "__main__":
    with app.app_context():
        Doctor.query.delete()
        Patient.query.delete()
        Appointment.query.delete()
        doctors: list[Doctor] = []
        for _ in range(10):
            doctors.append(
                Doctor(
                    name="Dr. " + fake.name(),
                    specialty=choice(
                        ["Humour imbalance", "Blood Letting", "Tranquilization"]
                    ),
                )
            )

        db.session.add_all(doctors)
        db.session.commit()

        patients = []
        for _ in range(10):
            patients.append(Patient(name=fake.name()))
        db.session.add_all(patients)
        db.session.commit()

        appointments = []

        for _ in range(10):
            weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            appointments.append(
                Appointment(
                    day=choice(weekdays),
                    doctor_id=choice(doctors).id,
                    patient_id=choice(patients).id,
                )
            )
        db.session.add_all(appointments)
        db.session.commit()
