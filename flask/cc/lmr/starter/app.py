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

@app.get('/rights')
def get_rights():
    rights = Right.query.all()
    right_list = []
    for right in rights:
        right_list.append(right.to_dict(rules = ('-middles',)))
    return make_response(jsonify(right_list), 200)

@app.get('/rights/<int:id>')
def rights_by_id(id):
    right = Right.query.filter(Right.id == id).first()
    if not right:
        return make_response(jsonify({'Error': 'This right does not exist.'}), 404)
    return make_response(jsonify(right.to_dict()), 200)

@app.post('/lefts')
def post_left():
    data = request.json
    try:
        new_left = Left(column = data.get('column'))
        db.session.add(new_left)
        db.session.commit()
        return make_response(jsonify(new_left.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify({'Error': 'Bad post request. ' + str(e)}), 405)

@app.patch('/middles/<int:id>')
def update_middle(id):
    middle = Middle.query.filter(Middle.id == id).first()
    if not middle:
        return make_response(jsonify({'Error': 'This middle does not exist.'}), 404)
    data = request.json
    try:
        for key in data:
            setattr(middle, key, data[key])
        db.session.add(middle)
        db.session.commit()
        return make_response(jsonify(middle.to_dict(rules = ('-left', '-right'))), 201)
    except Exception as e:
        return make_response(jsonify({'Error': 'Bad request. ' + str(e)}), 405)

@app.delete('/lefts/<int:id>')
def delete_left(id):
    left = Left.query.filter(Left.id == id).first()
    if not left:
        return make_response(jsonify({'Error': 'This left does not exist.'}), 404)
    db.session.delete(left)
    db.session.commit()
    return make_response(jsonify({}), 201)

if __name__ == "__main__":
    app.run(port=5555, debug=True)