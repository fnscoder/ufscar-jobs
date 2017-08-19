from flask import render_template, flash, redirect, url_for
from app import app, db
from app.models.forms import LoginForm, RegistrationForm
from app.models.tables import User


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    form.validate_on_submit()

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
