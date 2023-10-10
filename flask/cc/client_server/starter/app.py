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

# HELPPPPP
@app.get('/clients')
def get_clients():
    clients = Client.query.all()
    client_list = []
    for client in clients:
        client_list.append(client.to_dict(rules = ('-messages_list',)))
    server_dict_list = [server.to_dict() for server in client.servers]
    client_list['servers'] = server_dict_list
    return make_response(jsonify(client_list), 200)

@app.delete('/messages/<int:id>')
def delete_message(id):
    message = Message.query.filter(Message.id == id).first()
    if not message:
        return make_response(jsonify({'Error': 'Message does not exist.'}), 404)
    return make_response(jsonify({}), 201)

@app.post('/messages')
def new_message():
    data = request.json
    try:
        new_message = Message(content = data.get('content'), server_id = data.get('server_id'), client_id = data.get('client_id'))
        db.session.add(new_message)
        db.session.commit()
        return make_response(jsonify(new_message.to_dict(rules = ('-client_id', '-server_id'))), 201)
    except Exception as e:
        return make_response(jsonify({'Error': 'Bad message request. ' + str(e)}), 405)

@app.post('/servers')
def new_server():
    data = request.json
    try:
        new_server = Server(name = data.get('name'))
        db.session.add(new_server)
        db.session.commit()
        return make_response(jsonify(new_server.to_dict(rules = ('-messages_list',))), 201)
    except Exception as e:
        return make_response(jsonify({'Error': 'Bad server request. ' + str(e)}), 405)

@app.patch('/messages/<int:id>')
def update_message(id):
    message = Message.query.filter(Message.id == id).first()
    if not message:
        return make_response(jsonify({'Error': 'Message does not exist.'}), 404)
    data = request.json
    try:
        for key in data:
            setattr(message, key, data[key])
        db.session.add(message)
        db.session.commit()
        return make_response(jsonify(message.to_dict(rules = ('-client', '-server', '-server_id', '-client_id'))), 201)
    except Exception as e:
        return make_response(jsonify({'Error': 'Bad message update request. ' + str(e)}), 405)
    
if __name__ == "__main__":
    app.run(port=5555, debug=True)