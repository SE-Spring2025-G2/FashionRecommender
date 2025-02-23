from urllib import response
from flask import Flask, g
import json
from website.auth import auth
from website.auth import db
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import sys
from website.models import User

sys.path.append("..")

def login_user(client):
    mimetype = "application/x-www-form-urlencoded"
    headers = {"Content-Type": mimetype, "Accept": mimetype}

    # This user is not present in the db
    data = {"email": "test@gmail.com", "password": "password123"}
    url = "/login"

    response = client.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return True
    return False

# running
def test_recommendations(app):
    client = app.test_client()

    data = {"occasion": "birthday", "city": "Raleigh"}

    url = "/recommendations"
    with client as c:
        var = c.post(url, data=data)
        assert var.status_code >= 200 and var.status_code < 400


#### [WIP] trying to mock DB
def test_recommendations_with_session(app):
    client = app.test_client()

    login_user(client)

    data = {"occasion": "birthday", "city": "Raleigh"}

    url = "/recommendations"
    with client as c:
        var = c.post(url, data=data)
        assert var.status_code >= 200 and var.status_code < 400
