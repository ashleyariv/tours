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

    serialize_rules = ("-message_list.server_object",)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    message_list = db.relationship(
        "Message", back_populates="server_object", cascade="all, delete-orphan"
    )
    clients = association_proxy("message_list", "client_object")

    @validates("name")
    def validate_name(self, key, name):
        uppers_set = set(string.ascii_uppercase)
        name_set = set(name)
        if not name.isupper() and len(name_set - uppers_set) > 0:
            raise ValueError("Server names must be upper case")
        return name


class Message(db.Model, SerializerMixin):
    __tablename__ = "message_table"

    serialize_rules = ("-server_object.message_list", "-client_object.message_list")
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

    server_id = db.Column(db.Integer, db.ForeignKey("server_table.id"), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client_table.id"), nullable=False)

    server_object = db.relationship("Server", back_populates="message_list")
    client_object = db.relationship("Client", back_populates="message_list")

    @validates("content")
    def validate_name(self, key, content):
        if not content:
            raise ValueError("Content must not be empty")
        return content


class Client(db.Model, SerializerMixin):
    serialize_rules = ("-message_list.client_object",)
    __tablename__ = "client_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    message_list = db.relationship(
        "Message", back_populates="client_object", cascade="all, delete-orphan"
    )
    servers = association_proxy("message_list", "server_object")
