from flask import Flask
from app import app
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
from wtforms.validators import Required
from wtforms import StringField, PasswordField,TextAreaField
from wtforms.validators import DataRequired

class UsernamePasswordForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RecordForm(FlaskForm):
    time = StringField('time', validators=[DataRequired()])
    record = TextAreaField('record', validators=[DataRequired()])
