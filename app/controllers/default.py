from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db, lm

from app.models.forms import LoginForm, RegistrationForm
from app.models.tables import User


@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logado com sucesso!")
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha inválidos.")

    return render_template('login.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.name.data, form.email.data, form.username.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Obrigado por se registrar!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Deslogado!")
    return redirect(url_for("index"))
