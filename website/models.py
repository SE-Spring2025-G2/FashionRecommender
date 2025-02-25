from . import db
from flask_login import UserMixin
from .CustomMixin import SerializerMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    gender = db.Column(db.String(20))
    phone_number = db.Column(db.Integer)
    password = db.Column(db.String(150))
    age = db.Column(db.Integer)
    city = db.Column(db.String(50))


class Preference(db.Model, UserMixin):
    userid = db.Column(db.Integer, primary_key=True)
    preferences = db.Column(db.Text)


class Favourite(db.Model, UserMixin, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    favourite_url = db.Column(db.String(255))
    search_occasion = db.Column(db.String(255))
    search_weather = db.Column(db.String(255))

class Feedback(db.Model, UserMixin, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    ftype = db.Column(db.String(100), nullable=False)
    comments = db.Column(db.Text, nullable=False)
    frate = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

class Searchhistory(db.Model, UserMixin, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    search_terms = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    search_links = db.Column(db.JSON, nullable=False)