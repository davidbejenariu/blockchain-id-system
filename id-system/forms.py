from wtforms import Form, StringField, BooleanField, DecimalField, IntegerField, TextAreaField, PasswordField, validators
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    name = StringField('Full name', [validators.Length(min=1, max=64)])
    # TODO validator
    email = StringField('Email', [validators.Length(min=6, max=64)])
    password = PasswordField('Password', [validators.input_required()])
    is_admin = BooleanField('Is Admin?')


class LoginForm(FlaskForm):
    email = StringField('Email', [validators.Length(min=6, max=64)])
    password = PasswordField('Password', [validators.input_required()])
