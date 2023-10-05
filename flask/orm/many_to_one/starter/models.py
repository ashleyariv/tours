from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = "user_table"
    #serialize rules = ('-relationship_object.other_relationship_object')
    serialize_rules = ('-blog_list.user_object',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    blog_list = db.relationship('Blog', back_populates = 'user_object')

    # def to_dict(self):
    #     return {'id': self.id, 'name': self.name}





class Blog(db.Model, SerializerMixin):
    __tablename__ = "blog_table"
    serialize_rules = ('-user_object.blog_list',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))

    user_object = db.relationship('User', back_populates = 'blog_list')

    # def to_dict(self):
    #     return {'id': self.id, 'title': self.title, 'content': self.content, 'user_id': self.user_id}






