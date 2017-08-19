from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, Form, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class RegistrationForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(message="Informe o nome.")])
    email = StringField("email", validators=[DataRequired(message="Informe o e-mail.")])
    username = StringField("username", validators=[DataRequired(message="Informe o nome de usuário.")])
    password = PasswordField("password", [validators.DataRequired(message="Informe a senha."), validators.EqualTo("confirm", message="As senhas devem ser iguais")])
    confirm = PasswordField("confirm", validators=[DataRequired(message="Informe a senha novamente.")])


class EditForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(message="Informe o nome.")])
    email = StringField("email", validators=[DataRequired(message="Informe o e-mail.")])
    username = StringField("username", validators=[DataRequired(message="Informe o nome de usuário.")])
    password = PasswordField("password", [validators.DataRequired(message="Informe a senha."), validators.EqualTo("confirm", message="As senhas devem ser iguais")])
    confirm = PasswordField("confirm", validators=[DataRequired(message="Informe a senha novamente.")])
