from flask import make_response, jsonify, request, g
from flask import Flask
from models import db, User, Blog
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def root():
    return "<h1>Simple blog site</h1>"


@app.get("/users")
def get_users():
    users = User.query.all()
    user_json_list = []
    for user in users:
        user_json_list.append(user.to_dict())
    #list comprehension for the above code, this does the same thing
    #user_json_list = [user.to_dict() for user in users]
    return make_response(jsonify(user_json_list), 200)


@app.post("/users")
def post_user():
    request_data = request.json 
    new_user = User(name = request_data['name'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify(new_user.to_dict()), 201)


@app.get("/users/<int:id>")
def get_user_by_id(id: int):
    user = User.query.filter(User.id == id).first()
    if user is None:
        return make_response(jsonify({'error': f'no user with id {id}'}, 404))
    return make_response(jsonify(user.to_dict()), 200)


@app.get("/users/<int:id>/blogs")
def get_blogs_for_user(id: int):
    #Blog.query.filter(Blog.user_id == id).all()
    user = User.query.filter(User.id == id).first()
    blogs = user.blog_list
    blogs_json = [blog.to_dict() for blog in blogs]

    return make_response(jsonify(blogs_json), 200)


@app.post("/users/<int:id>/blogs")
def post_blog_for_user(id: int):
    return {}


@app.get("/blogs/<int:id>")
def get_blog_by_id(id: int):
    return {}


@app.patch("/blogs/<int:id>")
def patch_blog(id: int):
    return {}


@app.patch("/users/<int:id>")
def patch_user(id: int):
    data = request.json
    user = User.query.filter(User.id == id).first()
    # {'name': 'something'}
    for key in data:
        # key => 'name'
        # data[key] => 'something'
        # >> user.name = 'something'
        setattr(user, key, data[key])
    db.session.add(user)
    db.session.commit()
    return make_response(jsonify(user.to_dict()), 201)


@app.delete("/blogs/<int:id>")
def delete_blog(id: int):
    return {}


@app.delete("/users/<int:id>")
def delete_user(id: int):
    user = User.query.filter(User.id == id).first()
    #check that user was found
    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({}), 200)




if __name__ == "__main__":
    app.run(port=5555, debug=True)
