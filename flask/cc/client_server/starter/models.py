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


class Server(db.Model, SerializerMixin):
    __tablename__ = "server_table"

    id = db.Column(db.Integer, primary_key=True)



class Message(db.Model, SerializerMixin):
    __tablename__ = "message_table"

    id = db.Column(db.Integer, primary_key=True)


class Client(db.Model, SerializerMixin):
    __tablename__ = "client_table"
    id = db.Column(db.Integer, primary_key=True)

