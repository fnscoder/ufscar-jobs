from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, Form, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class RegistrationForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", [validators.DataRequired(), validators.EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("confirm", validators=[DataRequired()])
