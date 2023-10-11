#!/usr/bin/env python3

from app import app
from models import db  # models go here
from faker import Faker
from random import randint, choice, choices
from models import Right, Left, Middle
import string

fake = Faker()

if __name__ == "__main__":
    with app.app_context():
        Right.query.delete()
        Middle.query.delete()
        Left.query.delete()


        rights = []
        for _ in range(10):
            rights.append(Right(column="".join(choices(string.digits, k=5))))
        db.session.add_all(rights)
        db.session.commit()

        lefts = []
        for _ in range(10):
            lefts.append(Left(column="".join(choices(string.ascii_letters, k=5))))
        db.session.add_all(lefts)
        db.session.commit()

        middles = []

        for _ in range(10):
            middles.append(
                Middle(
                    column="".join(choices(string.punctuation, k=5)),
                    left_id=choice(lefts).id,
                    right_id=choice(rights).id,
                )
            )
        db.session.add_all(middles)
        db.session.commit()
