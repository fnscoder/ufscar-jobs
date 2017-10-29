from flask import render_template, flash, request, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_weasyprint import HTML, render_pdf
from app import app, db, lm, mail, s, bcrypt

from app.models.forms import LoginForm, RegistrationForm, EditForm, InfoForm, \
    CourseForm, WorkForm, EditInfoForm, EditCourseForm, EditWorkForm, \
    InfoCompanyForm, EditInfoCompanyForm, JobForm, EditJobForm, SearchForm, ContactForm, EmailForm, NewPasswordForm
from app.models.tables import User, Info, Course, Work, Company, Job
from app.scraping_infojobs import get_http, get_jobs, get_page_job


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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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
        try:
            password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(form.name.data, form.email.data, form.username.data,
                        password, form.type_user.data)
            db.session.add(user)
            db.session.commit()
            flash('Obrigado por se registrar!')
            return redirect(url_for('login'))
        except:
            flash('Não foi possível realizar o cadastro. Verifique os dados e tente novamente.')
            flash('O nome de usuário e o e-mail devem ser únicos.')
            return render_template('register.html', form=form) 
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
@login_required
def profile(username):
    '''
    Exibe o perfil do usuário ou da empresa
    '''
    return render_template('profile.html')


@app.route("/edit/<username>", methods=["GET", "POST"])
@login_required
def edit_profile(username):
    '''
    Edita as informações de registro do usuário ou empresa
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
@login_required
def info(username):
    '''
    Carrega o formulário de informações do usuários (dados pessoais)
    Verifica se já existem informações gravadas para o usuário logado,
    senão tiver carrega o formulário e redireciona para a url de adicionar
    informações. Se já tiver informações salvas exibe as informações
    '''
    if current_user.type_user == 1:
        form = InfoForm()
        i = Info.query.filter_by(user_id=current_user.id).first()
        if i:
            return render_template('info.html', i=i)
        else:
            if request.method == "POST" and form.validate_on_submit():
                info = Info(form.birth_date.data, form.alternative_email.data,
                            form.phone.data, form.cellphone.data,
                            form.cpf.data, form.street.data, form.number.data,
                            form.city.data, form.state.data, form.cep.data,
                            current_user.id)
                db.session.add(info)
                db.session.commit()
                flash('Informações inseridas com sucesso!')
                return redirect(url_for(
                    'info', username=current_user.username))
        return render_template('add_info.html', form=form)
    else:
        return render_template('erro.html')


@app.route("/edit_info/<username>", methods=["GET", "POST"])
@login_required
def edit_info(username):
    '''
    Carrega o formulário com as informações do usuário para permitir a edição
    das informações
    '''
    if current_user.type_user == 1:
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
    else:
        return render_template('erro.html')


@app.route("/add_course/<username>", methods=["GET", "POST"])
@login_required
def add_course(username):
    '''
    Permite adicionar cursos para o usuário logado
    '''
    if current_user.type_user == 1:
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
    else:
        return render_template('erro.html')


@app.route("/add_work/<username>", methods=["GET", "POST"])
@login_required
def add_work(username):
    '''
    Permte adicionar experiencia profissional para o usuario logado
    '''
    if current_user.type_user == 1:
        form = WorkForm()
        if request.method == "POST" and form.validate_on_submit():
            work = Work(form.post.data, form.company.data,
                        form.entry_date.data, form.departure_date.data,
                        form.tasks.data, form.observation.data,
                        current_user.id)
            db.session.add(work)
            db.session.commit()
            flash('Informações inseridas com sucesso!')
            return redirect(url_for('works', username=current_user.username))
        return render_template('add_work.html', form=form)
    else:
        return render_template('erro.html')


@app.route("/edit_course/<username>", methods=["GET", "POST"])
@login_required
def edit_course(username):
    '''
    Rota para edição das informações de um curso específico do usuário
    '''
    if current_user.type_user == 1:
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
    else:
        return render_template('erro.html')


@app.route("/edit_work/<username>", methods=["GET", "POST"])
@login_required
def edit_work(username):
    '''
    Edita informações de uma exp profissional do usuário
    '''
    if current_user.type_user == 1:
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
    else:
        return render_template('erro.html')


@app.route("/courses/<username>", methods=["GET", "POST"])
@login_required
def courses(username):
    '''
    Exibe os cursos de um usuário
    '''
    if current_user.type_user == 1:
        my_courses = Course.query.filter_by(user_id=current_user.id)
        return render_template('courses.html', courses=my_courses)
    else:
        return render_template('erro.html')


@app.route("/works/<username>", methods=["GET", "POST"])
@login_required
def works(username):
    '''
    Exibe os trabalhos de um usuário
    '''
    if current_user.type_user == 1:
        my_works = Work.query.filter_by(user_id=current_user.id)
        return render_template('works.html', works=my_works)
    else:
        return render_template('erro.html')


@app.route("/delete_course/<int:id>", methods=["GET", "POST"])
@login_required
def delete_course(id):
    '''
    Permite deletar um curso específico
    '''
    if current_user.type_user == 1:
        c = Course.query.filter_by(id=id).first()
        db.session.delete(c)
        db.session.commit()

        return redirect(url_for('courses', username=current_user.username))
    else:
        return render_template('erro.html')


@app.route("/delete_work/<int:id>", methods=["GET", "POST"])
@login_required
def delete_work(id):
    '''
    Permite deletar uma exp profissional
    '''
    if current_user.type_user == 1:
        w = Work.query.filter_by(id=id).first()
        db.session.delete(w)
        db.session.commit()

        return redirect(url_for('works', username=current_user.username))
    else:
        return render_template('erro.html')


@app.route("/company_info/<username>", methods=["GET", "POST"])
@login_required
def company_info(username):
    '''
    Verifica se o perfil é de empresa ou candidato, se for empresa
    Carrega o formulário de informações da empresa
    Verifica se já existem informações gravadas para empresa logada,
    senão tiver carrega o formulário e redireciona para a url de adicionar
    informações. Se já tiver informações salvas exibe as informações
    '''
    if current_user.type_user == 2:
        form = InfoCompanyForm()
        c = Company.query.filter_by(user_id=current_user.id).first()
        if c:
            return render_template('company_info.html', c=c)
        else:
            if request.method == "POST" and form.validate_on_submit():
                company = Company(form.cnpj.data, form.phone.data,
                                  form.street.data, form.number.data,
                                  form.city.data, form.state.data,
                                  form.cep.data, current_user.id)
                db.session.add(company)
                db.session.commit()
                flash('Informações inseridas com sucesso!')
                return redirect(url_for(
                    'company_info', username=current_user.username))
        return render_template('add_company_info.html', form=form)
    else:
        return render_template('erro.html')


@app.route("/edit_company_info/<username>", methods=["GET", "POST"])
@login_required
def edit_company_info(username):
    '''
    Carrega o formulário com as informações da empresa para permitir a edição
    das informações
    '''
    if current_user.type_user == 2:
        form = EditInfoCompanyForm()
        c = Company.query.filter_by(user_id=current_user.id).first()
        if request.method == "POST":

            c.cnpj = request.form.get("cnpj")
            c.phone = request.form.get("phone")
            c.street = request.form.get("street")
            c.number = request.form.get("number")
            c.city = request.form.get("city")
            c.state = request.form.get("state")
            c.cep = request.form.get("cep")

            db.session.commit()
            flash('Informações atualizadas com sucesso!')
            return redirect(url_for(
                'company_info', username=current_user.username))
        return render_template('edit_company_info.html', form=c)
    else:
        return render_template('erro.html')


@app.route("/add_job/<username>", methods=["GET", "POST"])
@login_required
def add_job(username):
    '''
    Permite que a empresa adicione uma vaga
    '''
    if current_user.type_user == 2:
        form = JobForm()
        if request.method == "POST" and form.validate_on_submit():
            job = Job(form.title.data, form.description.data, current_user.id)
            db.session.add(job)
            db.session.commit()
            flash('Informações inseridas com sucesso!')
            return redirect(url_for('jobs', username=current_user.username))
        return render_template('add_job.html', form=form)
    else:
        return render_template('erro.html')


@app.route("/jobs/<username>", methods=["GET", "POST"])
@login_required
def jobs(username):
    '''
    Exibe as vagas postadas pela empresa
    '''
    if current_user.type_user == 2:
        j = Job.query.filter_by(user_id=current_user.id)
        return render_template('jobs.html', jobs=j)
    else:
        return render_template('erro.html')


@app.route("/edit_job/<int:id>", methods=["GET", "POST"])
@login_required
def edit_job(id):
    '''
    Edita informações de uma vaga postada
    '''
    if current_user.type_user == 2:
        form = EditJobForm()
        j = Job.query.filter_by(id=id).first()
        if request.method == "POST":
            j.title = request.form.get('title')
            j.description = request.form.get('description')

            db.session.commit()
            flash('Atualizado!')

            return redirect(url_for('jobs', username=current_user.username))
        return render_template('edit_job.html', form=j)
    else:
        return render_template('erro.html')


@app.route("/delete_job/<int:id>", methods=["GET", "POST"])
@login_required
def delete_job(id):
    '''
    Permite deletar uma exp profissional
    '''
    if current_user.type_user == 2:
        j = Job.query.filter_by(id=id).first()
        db.session.delete(j)
        db.session.commit()

        return redirect(url_for('jobs', username=current_user.username))
    else:
        return render_template('erro.html')


@app.route("/all_jobs", methods=["GET", "POST"])
def all_jobs():
    j = Job.query.all()
    return render_template('all_jobs.html', all_jobs=j)


@app.route("/job_description/<int:id>", methods=["GET", "POST"])
def job_description(id):

    job = Job.query.filter_by(id=id).first()
    company = User.query.filter_by(id=job.user_id).first()
    company = company.name

    j = {
        'title': job.title,
        'company': company,
        'description': job.description
    }
    return render_template('job_description.html', j=j)


@app.route("/search_jobs", methods=["GET", "POST"])
def search_jobs(search=None):
    form = SearchForm()
    if request.method == "POST":
        search = request.form.get('search')

        return redirect(url_for('search_outjobs', search=search))
    return render_template('search_jobs.html', form=form)


@app.route("/search_outjobs/<search>", methods=["GET", "POST"])
def search_outjobs(search):
    r = get_http(search)

    if r:
        jobs_list = get_jobs(r.text)
        jobs = get_page_job(jobs_list)
    return render_template('search_outjobs.html', jobs=jobs)


@app.route("/list_candidates", methods=["GET", "POST"])
def list_candidates():
    '''
    Exibe os candidatos cadastrados
    Exibe apenas para perfis de empresas
    '''
    c = User.query.filter_by(type_user=1).all()
    return render_template('candidates.html', candidates=c)
   

@app.route("/candidate_details/<int:id>", methods=["GET", "POST"])
def candidate_details(id):
    '''
    Exibe os detalhes de um candidato
    Exibe apenas para perfis de empresas
    '''
    user = User.query.filter_by(id=id).first()
    courses = Course.query.filter_by(user_id=id)
    works = Work.query.filter_by(user_id=id)

    candidate = {
        'user': user,
        'courses': courses,
        'works': works
    }
    return render_template('candidate_details.html', c=candidate)


@app.route("/search_insite_jobs", methods=["GET", "POST"])
def search_insite_jobs():
    '''
    Busca as vagas no db conforme o parâmetro job passado
    '''
    form = SearchForm()
    if request.method == "POST":
        job = form.search.data
        jobs = Job.query.filter(Job.description.like("%"+job+"%")).all()
        for j in jobs:
            print(j)
        return render_template('found_insite_jobs.html', jobs=jobs)
    else:
        return render_template('search_insite_jobs.html', form=form)


@app.route("/search_candidates", methods=["GET", "POST"])
def search_candidates():
    form = SearchForm()
    if request.method == "POST":
        if current_user.type_user == 2:
            c = User.query.filter_by(email=form.search.data).all()
            return render_template('found_candidates.html', candidates=c)
        else:
            return render_template('erro.html')
    return render_template('search_candidates.html', form=form)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if request.method == "POST" and form.validate_on_submit():
        
        name = request.form['name']
        email = request.form['email']
        subject = '[Contato - UfscarJobs] - {}'.format(request.form['subject'])
        message = request.form['message']
        msg = Message(subject, sender=email, recipients=['ufscarjobs@gmail.com'])
        msg.body = 'Nova mensagem de {}\nE-mail de contato: {}\nAssunto: {}\nMensagem: {}'.format(name, email, subject, message)
        mail.send(msg)
        flash('Mensagem envida!')
        return redirect(url_for('index'))
    return render_template('contact.html', form=form)


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    form = EmailForm()
    if request.method == "POST" and form.validate_on_submit():
        email = request.form['email']

        if User.query.filter_by(email=email).first():

            token = s.dumps(email, salt='forgot_password')
            msg = Message('[Ufscar Jobs] - Esqueceu sua senha', sender='ufscarjobs@gmail.com', recipients=[email])
            link = url_for('new_password', token=token, _external=True)
            msg.body = 'Para definir uma nova senha clique no link abaixo:\n{}\nSe o link não funcionar copie e cole o endereço em seu navegador'.format(link)
            mail.send(msg)
            flash('Mensagem envida! Verifique seu e-mail.')
            return redirect(url_for('index'))
        flash('E-mail não encontrado.')
        return redirect(url_for('forgot_password'))
        
    return render_template('forgot_password.html', form=form)


@app.route('/new_password/<token>', methods=["GET", "POST"])
def new_password(token):
    form = NewPasswordForm()
    try:
        email = s.loads(token, salt='forgot_password', max_age=3600)
        if request.method == "POST" and form.validate_on_submit():
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
            user.password = password
            db.session.commit()
            flash('Senha alterada com sucesso!')
            return redirect(url_for('index'))
            
        return render_template('new_password.html', form=form)
                
    except SignatureExpired:
        flash('Solicitação expirada!')
        return redirect(url_for('index'))
        

@app.route("/all_jobs_pdf", methods=["GET", "POST"])
def all_jobs_pdf():
    j = Job.query.all()
    return render_template('all_jobs_pdf.html', all_jobs=j)


@app.route('/jobs.pdf')
def jobs_pdf():
    return render_pdf(url_for('all_jobs_pdf'))


@app.route("/list_candidates_pdf", methods=["GET", "POST"])
def list_candidates_pdf():
    '''
    Exibe os candidatos cadastrados
    '''
    c = User.query.filter_by(type_user=1).all()
    return render_template('candidates_pdf.html', candidates=c)


@app.route('/candidates.pdf')
def candidates_pdf():
    return render_pdf(url_for('list_candidates_pdf'))
