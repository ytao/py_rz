from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import chartkick

app = Flask(__name__,instance_relative_config=True)
app.jinja_env.add_extension("chartkick.ext.charts")
# app.config.from_object('config')
app.config.from_pyfile('pyconf.py')



db = SQLAlchemy(app)

from app import views

# vim: set fdc=2:
