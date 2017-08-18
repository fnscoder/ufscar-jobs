from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User %r>" % self.username


class Info(db.Model):
    __tablename__ = "infos"

    id = db.Column(db.Integer, primary_key=True)
    birth_date = db.Column(db.DateTime)
    alternative_email = db.Column(db.String(150))
    phone = db.Column(db.String(20), nullable=False)
    cellphone = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.Integer, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, birth_date, alternative_email, phone, cellphone,
                 cpf, user_id):
        self.birth_date = birth_date
        self.alternative_email = alternative_email
        self.phone = phone
        self.cellphone = cellphone
        self.cpf = cpf
        self.user_id = user_id

    def __repr__(self):
        return "<Info %r>" % self.id


class Address(db.Model):
    __tablename__ = "adresses"

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(150), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    cep = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, street, number, city, state, cep, user_id):
        self.street = street
        self.number = number
        self.city = city
        self.state = state
        self.cep = cep
        self.user_id = user_id

    def __repr__(self):
        return "<Address - City %r>" % self.city


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), nullable=False)
    school_name = db.Column(db.String(150), nullable=False)
    grade = db.Column(db.String(30), nullable=False)
    course_load = db.Column(db.Integer, nullable=False)
    conclusion = db.Column(db.DateTime, nullable=False)
    observation = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, course_name, school_name, grade, course_load,
                 conclusion, observation, user_id):
        self.course_name = course_name
        self.school_name = school_name
        self.grade = grade
        self.course_load = course_load
        self.conclusion = conclusion
        self.observation = observation
        self.user_id = user_id

    def __repr__(self):
        return "<Course %r>" % self.course_name


class Work(db.Model):
    __tablename__ = "works"

    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False)
    departure_date = db.Column(db.DateTime)
    tasks = db.Column(db.String(250), nullable=False)
    observation = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, post, company, entry_date, departure_date, tasks,
                 observation, user_id):
        self.post = post
        self.company = company
        self.entry_date = entry_date
        self.departure_date = departure_date
        self.tasks = tasks
        self.observation = observation
        self.user_id = user_id

    def __repr__(self):
        return "<Post %r>" % self.post