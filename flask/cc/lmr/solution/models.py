from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import string

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Left(db.Model, SerializerMixin):
    __tablename__ = "left_table"

    serialize_rules = ("-middles.left",)
    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.String, nullable=False, unique=True)

    middles = db.relationship(
        "Middle", back_populates="left", cascade="all, delete-orphan"
    )
    rights = association_proxy("middles", "right")

    @validates("column")
    def validate_column(self, key, column):
        if not column.isalpha():
            raise ValueError("column must be letters")
        return column


class Middle(db.Model, SerializerMixin):
    __tablename__ = "middle_table"

    serialize_rules = ("-left.middles", "-right.middles")
    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.String, nullable=False)

    left_id = db.Column(db.Integer, db.ForeignKey("left_table.id"), nullable=False)
    right_id = db.Column(db.Integer, db.ForeignKey("right_table.id"), nullable=False)

    left = db.relationship("Left", back_populates="middles")
    right = db.relationship("Right", back_populates="middles")

    @validates("column")
    def validate_column(self, key, column):
        if column.isalpha() or column.isdigit() or column == "":
            raise ValueError("column must be punctuation")
        return column


class Right(db.Model, SerializerMixin):
    __tablename__ = "right_table"
    serialize_rules = ("-middles.right",)
    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.String, nullable=False, unique=True)

    middles = db.relationship(
        "Middle", back_populates="right", cascade="all, delete-orphan"
    )
    lefts = association_proxy("middles", "left")

    @validates("column")
    def validate_column(self, key, column):
        if not column.isdigit():
            raise ValueError("column must be digits")
        return column
