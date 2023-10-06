from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import string, datetime

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)


class Patient(db.Model, SerializerMixin):
    __tablename__ = "patient_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # -list.object
    serialize_rules = ("-appointments.patient_object",)
    appointments = db.relationship(
        "Appointment", back_populates="patient_object", cascade="all, delete-orphan"
    )
    doctors = association_proxy("appointments", "doctor_object")


class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointment_table"

    # -object1.list -object2.list
    serialize_rules = ("-patient_object.appointments", "-doctor_object.appointments")

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String)

    patient_id = db.Column(
        db.Integer, db.ForeignKey("patient_table.id"), nullable=False
    )
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_table.id"), nullable=False)

    patient_object = db.relationship("Patient", back_populates="appointments")
    doctor_object = db.relationship("Doctor", back_populates="appointments")

    @validates("day")
    def validate_date(self, key, day):
        if day not in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
            raise ValueError("appointments must be on a weekday")
        return day


class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctor_table"
    serialize_rules = ("-appointments.doctor_object",)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    specialty = db.Column(db.String, nullable=False)

    appointments = db.relationship(
        "Appointment", back_populates="doctor_object", cascade="all, delete-orphan"
    )
    patients = association_proxy("appointments", "patient_object")

    @validates("name")
    def validate_name(self, key, name):
        if not name.startswith("Dr."):
            raise ValueError("You can't hire a quack!")
        return name
