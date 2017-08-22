from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from app import app, db, lm

from app.models.forms import LoginForm, RegistrationForm, EditForm, InfoForm, CourseForm, WorkForm, EditInfoForm, EditCourseForm, EditWorkForm
from app.models.tables import User, Info, Course, Work


@lm.user_loader
def load_user(id):
    '''
    Função que retorna o usuário logado no momento
    '''
    return User.query.filter_by(id=id).first()


'''
Definição das rotas da aplicação
'''


@app.route("/")
def index():
    '''
    Rota para o index.html
    '''
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    '''
    Rota para o login, chama o formulário de login e valida o form
    se for válido carrega as informações na variavel user e verifica
    se o user e password estão corretos
    '''
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
    '''
    Rota para o registro de usuários
    carrega o form de registro, se for um arequisição post e
    o form for válido carrega as infos no user e usa o db.session.add(user)
    para adicionar a sessão do db e o db.session.commit() para gravar no
    banco
    '''
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User(form.name.data, form.email.data, form.username.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Obrigado por se registrar!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/logout")
def logout():
    '''
    Desloga o usuário com a função logout_user()
    '''
    logout_user()
    flash("Deslogado!")
    return redirect(url_for("index"))


@app.route("/profile/<username>")
def profile(username):
    '''
    Exibe o perfil do usuário
    '''
    return render_template('profile.html')


@app.route("/edit/<username>", methods=["GET", "POST"])
def edit_profile(username):
    '''
    Edita as informações de registro do usuário
    '''
    form = EditForm()
    if request.method == "POST" and form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.password = form.password.data

        db.session.commit()
        flash('Atualizado!')
        return redirect(url_for('profile', username=current_user.username))
    return render_template('edit_profile.html', form=form)


@app.route("/info/<username>", methods=["GET", "POST"])
def info(username):
    '''
    Carrega o formulário de informações do usuários (dados pessoais)
    Verifica se já existem informações gravadas para o usuário logado,
    senão tiver carrega o formulário e redireciona para a url de adicionar
    informações. Se já tiver informações salvas exibe as informações
    '''
    form = InfoForm()
    i = Info.query.filter_by(user_id=current_user.id).first()
    if i:
        return render_template('info.html', i=i)
    else:
        if request.method == "POST" and form.validate_on_submit():
            info = Info(form.birth_date.data, form.alternative_email.data,
                        form.phone.data, form.cellphone.data, form.cpf.data,
                        form.street.data, form.number.data, form.city.data,
                        form.state.data, form.cep.data, current_user.id)
            db.session.add(info)
            db.session.commit()
            flash('Informações inseridas com sucesso!')
            return redirect(url_for('info', username=current_user.username))
    return render_template('add_info.html', form=form)


@app.route("/edit_info/<username>", methods=["GET", "POST"])
def edit_info(username):
    '''
    Carrega o formulário com as informações do usuário para permitir a edição
    das informações
    '''
    form = EditInfoForm()
    i = Info.query.filter_by(user_id=current_user.id).first()
    if request.method == "POST":
        i.birth_date = request.form.get("birth_date")
        i.alternative_email = request.form.get("alternative_email")
        i.phone = request.form.get("phone")
        i.cellphone = request.form.get("cellphone")
        i.cpf = request.form.get("cpf")
        i.street = request.form.get("street")
        i.number = request.form.get("number")
        i.city = request.form.get("city")
        i.state = request.form.get("state")
        i.cep = request.form.get("cep")

        db.session.commit()
        flash('Informações atualizadas com sucesso!')
        return redirect(url_for('info', username=current_user.username))
    return render_template('edit_info.html', form=i)


@app.route("/add_course/<username>", methods=["GET", "POST"])
def add_course(username):
    '''
    Permite adicionar cursos para o usuário logado
    '''
    form = CourseForm()
    if request.method == "POST" and form.validate_on_submit():
        course = Course(form.course_name.data, form.school_name.data,
                        form.grade.data, form.course_load.data,
                        form.conclusion.data, form.observation.data,
                        current_user.id)
        db.session.add(course)
        db.session.commit()
        flash('Informações inseridas com sucesso!')
        return redirect(url_for('courses', username=current_user.username))
    return render_template('add_course.html', form=form)


@app.route("/add_work/<username>", methods=["GET", "POST"])
def add_work(username):
    '''
    Permte adicionar experiencia profissional para o usuario logado
    '''
    form = WorkForm()
    if request.method == "POST" and form.validate_on_submit():
        work = Work(form.post.data, form.company.data,
                    form.entry_date.data, form.departure_date.data,
                    form.tasks.data, form.observation.data, current_user.id)
        db.session.add(work)
        db.session.commit()
        flash('Informações inseridas com sucesso!')
        return redirect(url_for('works', username=current_user.username))
    return render_template('add_work.html', form=form)


@app.route("/edit_course/<username>", methods=["GET", "POST"])
def edit_course(username):
    '''
    Rota para edição das informações de um curso específico do usuário
    '''
    form = EditCourseForm()
    c = Course.query.filter_by(user_id=current_user.id).first()
    if request.method == "POST":
        c.course_name = request.form.get("course_name")
        c.school_name = request.form.get("school_name")
        c.grade = request.form.get("grade")
        c.course_load = request.form.get("course_load")
        c.conclusion = request.form.get("conclusion")
        c.observation = request.form.get("observation")

        db.session.commit()
        flash('Atualizado!')
        return redirect(url_for('courses', username=current_user.username))
    return render_template('edit_course.html', form=c)


@app.route("/edit_work/<username>", methods=["GET", "POST"])
def edit_work(username):
    '''
    Edita informações de uma exp profissional do usuário
    '''
    form = EditWorkForm()
    w = Work.query.filter_by(user_id=current_user.id).first()
    if request.method == "POST":
        w.post = request.form.get('post')
        w.company = request.form.get('company')
        w.entry_date = request.form.get('entry_date')
        w.departure_date = request.form.get('departure_date')
        w.tasks = request.form.get('tasks')
        w.observation = request.form.get('observation')

        db.session.commit()
        flash('Atualizado!')
        return redirect(url_for('works', username=current_user.username))
    return render_template('edit_work.html', form=w)


@app.route("/courses/<username>", methods=["GET", "POST"])
def courses(username):
    '''
    Exibe os cursos de um usuário
    '''
    my_courses = Course.query.filter_by(user_id=current_user.id)
    return render_template('courses.html', courses=my_courses)


@app.route("/works/<username>", methods=["GET", "POST"])
def works(username):
    '''
    Exibe os trabalhos de um usuário
    '''
    my_works = Work.query.filter_by(user_id=current_user.id)
    return render_template('works.html', works=my_works)


@app.route("/delete_course/<int:id>", methods=["GET", "POST"])
def delete_course(id):
    '''
    Permite deletar um curso específico
    '''
    c = Course.query.filter_by(id=id).first()
    db.session.delete(c)
    db.session.commit()

    return render_template('courses.html', username=current_user.username)


@app.route("/delete_work/<int:id>", methods=["GET", "POST"])
def delete_work(id):
    '''
    Permite deletar uma exp profissional
    '''
    w = Work.query.filter_by(id=id).first()
    db.session.delete(w)
    db.session.commit()

    return render_template('works.html', username=current_user.username)
