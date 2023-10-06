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
    serialize_rules = ('-appointment_list. patient_object',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)

    appointment_list = db.relationship('Appointment', back_populates = 'patient_object', cascade = 'all, delete')
    doctors = association_proxy('appointment_list', 'doctor_object')

class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointment_table"
    serialize_rules = ('-patient_object.appointment_list', '-doctor_object.appointment_list')

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable = False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_table.id'), nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_table.id'), nullable = False)

    patient_object = db.relationship('Patient', back_populates = 'appointment_list')
    doctor_object = db.relationship('Doctor', back_populates = 'appointment_list')    

    @validates('day')
    def valid_day(self, key, day):
        if day == 'Saturday' or day == 'Sunday':
            raise ValueError('Day must not be a weekend.')
        return day

class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctor_table"
    serialize_rules = ('-appointment_list.doctor_object',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    specialty = db.Column(db.String, nullable = False)

    appointment_list = db.relationship('Appointment', back_populates = 'doctor_object', cascade = 'all, delete')
    patients = association_proxy('appointment_list', 'patient_object')

    @validates('name')
    def valid_name(self, key, name):
        if not name.startswith('Dr.'):
            raise ValueError('Doctor name must start with Dr.')
        return name