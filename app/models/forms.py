from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class RegistrationForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(
        message="Informe o nome.")])
    email = StringField("email", validators=[DataRequired(
        message="Informe o e-mail.")])
    username = StringField("username", validators=[DataRequired(
        message="Informe o nome de usuário.")])
    password = PasswordField("password", [validators.DataRequired(
        message="Informe a senha."), validators.EqualTo(
        "confirm", message="As senhas devem ser iguais")])
    confirm = PasswordField("confirm", validators=[DataRequired(
        message="Informe a senha novamente.")])


class EditForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(
        message="Informe o nome.")])
    email = StringField("email", validators=[DataRequired(
        message="Informe o e-mail.")])
    username = StringField("username", validators=[DataRequired(
        message="Informe o nome de usuário.")])
    password = PasswordField("password", [validators.DataRequired(
        message="Informe a senha."), validators.EqualTo(
        "confirm", message="As senhas devem ser iguais")])
    confirm = PasswordField("confirm", validators=[DataRequired(
        message="Informe a senha novamente.")])


class InfoForm(FlaskForm):
    birth_date = StringField("birth_date", validators=[DataRequired(
        message="Informe a data de nascimento.")])
    alternative_email = StringField("alternative_email", validators=[
        DataRequired(message="Informe o e-mail alternativo.")])
    phone = StringField("phone", validators=[DataRequired(
        message="Informe o telefone.")])
    cellphone = StringField("cellphone", validators=[DataRequired(
        message="Informe o celular.")])
    cpf = StringField("cpf", validators=[DataRequired(
        message="Informe o cpf.")])
    street = StringField("street", validators=[DataRequired(
        message="Informe o nome da rua.")])
    number = StringField("number", validators=[DataRequired(
        message="Informe o número.")])
    city = StringField("city", validators=[DataRequired(
        message="Informe a cidade.")])
    state = StringField("state", validators=[DataRequired(
        message="Informe o estado.")])
    cep = StringField("cep", validators=[DataRequired(
        message="Informe o cep.")])


class CourseForm(FlaskForm):
    course_name = StringField("course_name", validators=[DataRequired(
        message="Informe o nome do curso.")])
    school_name = StringField("school_name", validators=[
        DataRequired(message="Informe o nome da escola.")])
    grade = StringField("grade", validators=[DataRequired(
        message="Informe o tipo de curso.")])
    course_load = StringField("course_load", validators=[DataRequired(
        message="Informe a carga horária do curso.")])
    conclusion = StringField("conclusion", validators=[DataRequired(
        message="Informe a data de conclusão do curso.")])
    observation = StringField("observation")


class WorkForm(FlaskForm):
    post = StringField("post", validators=[DataRequired(
        message="Informe o cargo.")])
    company = StringField("company", validators=[
        DataRequired(message="Informe a empresa.")])
    entry_date = StringField("entry_date", validators=[DataRequired(
        message="Informe a data de entrada.")])
    departure_date = StringField("departure_date")
    tasks = StringField("tasks", validators=[DataRequired(
        message="Informe as atribuições do cargo.")])
    observation = StringField("observation")


class EditInfoForm(FlaskForm):
    birth_date = StringField("birth_date", validators=[DataRequired(
        message="Informe a data de nascimento.")])
    alternative_email = StringField("alternative_email", validators=[
        DataRequired(message="Informe o e-mail alternativo.")])
    phone = StringField("phone", validators=[DataRequired(
        message="Informe o telefone.")])
    cellphone = StringField("cellphone", validators=[DataRequired(
        message="Informe o celular.")])
    cpf = StringField("cpf", validators=[DataRequired(
        message="Informe o cpf.")])
    street = StringField("street", validators=[DataRequired(
        message="Informe o nome da rua.")])
    number = StringField("number", validators=[DataRequired(
        message="Informe o número.")])
    city = StringField("city", validators=[DataRequired(
        message="Informe a cidade.")])
    state = StringField("state", validators=[DataRequired(
        message="Informe o estado.")])
    cep = StringField("cep", validators=[DataRequired(
        message="Informe o cep.")])


class EditCourseForm(FlaskForm):
    course_name = StringField("course_name", validators=[DataRequired(
        message="Informe o nome do curso.")])
    school_name = StringField("school_name", validators=[
        DataRequired(message="Informe o nome da escola.")])
    grade = StringField("grade", validators=[DataRequired(
        message="Informe o tipo de curso.")])
    course_load = StringField("course_load", validators=[DataRequired(
        message="Informe a carga horária do curso.")])
    conclusion = StringField("conclusion", validators=[DataRequired(
        message="Informe a data de conclusão do curso.")])
    observation = StringField("observation")


class EditWorkForm(FlaskForm):
    post = StringField("post", validators=[DataRequired(
        message="Informe o cargo.")])
    company = StringField("company", validators=[
        DataRequired(message="Informe a empresa.")])
    entry_date = StringField("entry_date", validators=[DataRequired(
        message="Informe a data de entrada.")])
    departure_date = StringField("departure_date", validators=[DataRequired(
        message="Informe a data de saída.")])
    tasks = StringField("tasks", validators=[DataRequired(
        message="Informe as atribuições do cargo.")])
    observation = StringField("observation")
