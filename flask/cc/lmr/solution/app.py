#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Right, Left, Middle  # import your models here!

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.get("/")
def index():
    return "right/left"


@app.get("/rights")
def get_rights():
    rights = Right.query.all()
    return make_response(jsonify([r.to_dict(rules=("-middles",)) for r in rights]), 200)


@app.get("/rights/<int:id>")
def get_rights_by_id(id):
    right = db.session.get(Right, id)
    return make_response(jsonify(right.to_dict()), 200)


@app.post("/lefts")
def post_left():
    request_json = request.get_json()
    try:
        left = Left(
            column=request_json.get("column"),
        )
        db.session.add(left)
        db.session.commit()

        return make_response(jsonify(left.to_dict()), 202)
    except:
        return make_response(jsonify({"error": "could not instantiate left"}), 405)


@app.patch("/middles/<int:id>")
def patch_msg(id: int):
    msg = Middle.query.filter(Middle.id == id).first()
    if not msg:
        return make_response(jsonify({"error": "middle not found"}), 404)
    request_json = request.get_json()
    try:
        for key in request_json:
            setattr(msg, key, request_json.get(key))
        db.session.add(msg)
        db.session.commit()

        return make_response(
            jsonify(msg.to_dict(rules=("-left_object", "-right_object"))), 202
        )
    except ValueError:
        return make_response(jsonify({"error": "invalid middle patch"}), 405)


@app.delete("/lefts/<int:id>")
def delete_msg(id: int):
    left = Left.query.filter(Left.id == id).first()
    if not left:
        return make_response(jsonify({"error": "left not found"}), 404)
    db.session.delete(left)
    db.session.commit()
    return make_response(jsonify({}), 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
