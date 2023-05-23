from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, BooleanField


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        validators.DataRequired(),
        validators.Email()
    ])

    password = PasswordField('Password', validators=[
        validators.DataRequired()
    ])


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[
        validators.DataRequired(),
        validators.Length(min=3, max=50)
    ])

    email = StringField('Email', validators=[
        validators.DataRequired(),
        validators.Email()
    ])

    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d#@$!%*?&]{8,}$',
            message="Password must be at least 8 characters long, contain at least one uppercase letter, "
                    "one lowercase letter, one digit, and one special character."
        )
    ])

    is_admin = BooleanField('Is Admin?')
