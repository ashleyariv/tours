#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Client, Server, Message  # import your models here!

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.get("/")
def index():
    return "client/server"


@app.get("/clients")
def get_clients():
    clients = Client.query.all()
    client_list_json = []
    for client in clients:
        client_dict = client.to_dict(rules=("-message_list",))
        client_dict["servers"] = [
            s.to_dict(rules=("-message_list",)) for s in client.servers
        ]
        client_list_json.append(client_dict)
    return make_response(jsonify(client_list_json), 200)


@app.post("/messages")
def post_message():
    request_json = request.get_json()
    try:
        server = db.session.get(Server, request_json.get("server_id"))
        if not server:
            return make_response(
                jsonify({"error": "could not send message: invalid server"}), 405
            )
        client = db.session.get(Client, request_json.get("client_id"))
        if not client:
            return make_response(
                jsonify({"error": "could not send message: invalid client"}), 405
            )

        msg = Message(
            content=request_json.get("content"),
            server_object=server,
            client_object=client,
        )
        db.session.add(msg)
        db.session.commit()

        return make_response(
            jsonify(msg.to_dict(rules=("-server_id", "-client_id"))), 202
        )
    except:
        return make_response(jsonify({"error": "could not send message"}), 405)


@app.post("/servers")
def post_server():
    request_json = request.get_json()
    try:
        server = Server(
            name=request_json.get("name"),
        )
        db.session.add(server)
        db.session.commit()

        return make_response(jsonify(server.to_dict(rules=("-message_list",))), 202)
    except:
        return make_response(jsonify({"error": "could not instantiate server"}), 405)


@app.patch("/messages/<int:id>")
def patch_msg(id: int):
    msg = Message.query.filter(Message.id == id).first()
    if not msg:
        return make_response(jsonify({"error": "message not found"}), 404)
    request_json = request.get_json()
    try:
        for key in request_json:
            setattr(msg, key, request_json.get(key))
        db.session.add(msg)
        db.session.commit()

        return make_response(
            jsonify(msg.to_dict(rules=("-server_object", "-client_object"))), 202
        )
    except ValueError:
        return make_response(jsonify({"error": "invalid message edit"}), 405)


@app.delete("/messages/<int:id>")
def delete_msg(id: int):
    msg = Message.query.filter(Message.id == id).first()
    if not msg:
        return make_response(jsonify({"error": "message not found"}), 404)
    db.session.delete(msg)
    db.session.commit()
    return make_response(jsonify({}), 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
