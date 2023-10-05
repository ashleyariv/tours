from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
import re

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Student(db.Model, SerializerMixin):
    __tablename__ = "student_table"

    serialize_rules = ('-enrollment_list.student_object',)

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable = False)
    lname = db.Column(db.String, nullable = False)
    grad_year = db.Column(db.Integer, nullable = False)
    
    enrollment_list = db.relationship('Enrollment', back_populates = 'student_object', cascade = 'all, delete')
    courses = association_proxy('enrollment_list', 'course_object')

    @validates('grad_year')
    def valid_grad_year(self, key, year):
        if year < 2023:
            raise ValueError ('can not graduate in the past')
        return year


class Enrollment(db.Model, SerializerMixin):
    __tablename__ = "enrollment_table"

    serialize_rules = ('-student_object.enrollment_list', '-course_object.enrollment_list')

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_table.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course_table.id'))
    term = db.Column(db.String, nullable = False)

    student_object = db.relationship('Student', back_populates = 'enrollment_list')
    course_object = db.relationship('Course', back_populates = 'enrollment_list')

    @validates('term')
    def valid_term(self, key, term):
        if not (type(term) == str and term.startswith('S') or term.startswith('F') and term[1:].isdigit()):
            raise ValueError('term must start with S or F followed by a digit')
        return term

class Course(db.Model, SerializerMixin):
    __tablename__ = "course_table"
    serialize_rules = ('-enrollment_list.course_object',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)
    instructor = db.Column(db.String, nullable = False)
    credits = db.Column(db.Integer)

    enrollment_list = db.relationship('Enrollment', back_populates = 'course_object', cascade = 'all, delete')
    students = association_proxy('enrollment_list', 'student_object')

    @validates('title')
    def valid_title(self, key, title):
        if title == '':
            raise ValueError('title must not be empty')
        return title