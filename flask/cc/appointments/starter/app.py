#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
from models import db, Doctor, Patient, Appointment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.get("/")
def index():
    return "doctor/patient"

@app.get('/doctors')
def get_doctors():
    doctor_list = Doctor.query.all()
    doctor_json = []
    for doctor in doctor_list:
        doctor_json.append(doctor.to_dict(rules = ('-appointment_list',))) 
    return make_response(jsonify(doctor_json), 200)

@app.get('/doctors/<int:id>')
def doctors_by_id(id):
    doctor = Doctor.query.filter(Doctor.id == id).first()
    if not doctor:
        return make_response(jsonify({'Error': "Doctor does not exist."}), 404)
    return make_response(jsonify(doctor.to_dict(rules = ('-appointment_list.doctor_id', '-appointment_list.patient_id'))), 200)

@app.get('/patients/<int:id>')
def patients_by_id(id):
    patient = Patient.query.filter(Patient.id == id).first()
    if not patient:
        return make_response(jsonify({'Error': 'Patient does not exit.'}), 404)
    doctors_dict_list = [doctor.to_dict(rules = ('-appointment_list',)) for doctor in patient.doctors]
    patient_dict = patient.to_dict(rules = ('-appointment_list',))
    patient_dict['doctors'] = doctors_dict_list
    return make_response(jsonify(patient_dict), 200)

@app.delete('/appointments/<int:id>')
def delete_appointment(id):
    appointment = Appointment.query.filter(Appointment.id == id).first()
    if not appointment:
        return make_response(jsonify({'Error': 'Appointment does not exist.'}), 404)
    return make_response(jsonify({}),201)

@app.post('/doctors')
def new_doctor():
    data = request.json
    try:
        new_doctor = Doctor(name = data.get('name'), specialty = data.get('specialty'))
        db.session.add(new_doctor)
        db.session.commit()
        return make_response(new_doctor.to_dict(rules = ('-appointment_list',)), 201)
    except Exception as e:
        return make_response(jsonify({'Error': 'Bad doctor post. ' + str(e)}), 405)

@app.post('/appointments')
def new_appointment():
    data = request.json
    try:
        new_appointment = Appointment(day = data.get('day'), doctor_id = data.get('doctor_id'), patient_id = data.get('patient_id'))
        db.session.add(new_appointment)
        db.session.commit()
        return make_response(jsonify(new_appointment.to_dict(rules = ('-day', '-doctor_id', '-patient_id'))), 201)
    except Exception as e:
        return make_response(jsonify({'Error': 'Bad appointment post. ' + str(e)}), 405)

@app.patch('/patients/<int:id>')
def update_patient(id):
    patient = Patient.query.filter(Patient.id == id).first()
    if not patient:
        return make_response(jsonify({'Error': 'Patient does not exist.'}))
    data = request.json
    try:
        for key in data:
            setattr(patient, key, data[key])
        db.session.add(patient)
        db.session.commit()
        return make_response(jsonify(patient.to_dict(rules = ('-appointment_list',))), 201)
    except Exception as e:
        return make_response(jsonify({'Error': 'Bad update request. ' + str(e)}), 405)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
