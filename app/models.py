from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from app import app
from . import db

lm = LoginManager()
lm.init_app(app)
lm.session_protection = "strong"
lm.login_view =  "login"

@lm.user_loader
def load_user(userid):
    # return Admin.get_id(userid)
    return Admin.query.get(int(userid))
    # return Admin.query.filter(Admin.id==userid).first()

class User(db.Model):
    __tablename__ = 'main'
    # id   =db.Column(db.Integer, primary_key=True)
    date =db.Column(db.TEXT,primary_key=True, unique=False)
    text =db.Column(db.TEXT,primary_key=True, unique=False)
    def __init__(self, date, text):
        self.date = date
        self.text = text


    def __repr__(self):
        return self.date 

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password= db.Column(db.String(128), unique=False)


    def verify_password(self, password):
        if (password==self.password):
            return True
        else:
            return False

    def is_authenticated(self):
        return True
     
    def is_active(self):
        return True
     
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id

    def __repr__(self):
        return "<Admin '{:s}>".format(self.username)
    @property
    def name(self):
        return str(self.username)

# vim: set fdc=2:
