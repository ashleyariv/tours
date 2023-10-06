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


class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointment_table"


    id = db.Column(db.Integer, primary_key=True)


class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctor_table"

    id = db.Column(db.Integer, primary_key=True)

