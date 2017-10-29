import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


app = Flask(__name__)
app.config.from_object('config')

bcrypt = Bcrypt(app)
mail = Mail(app)
s = URLSafeTimedSerializer('total-secret')

# Utiliza o SQLAlchemy para criar e gerenciar o db e suas operações
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Comandos adicionais para facilitar o gerenciamento do db
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server())

# configuração do server
port = int(os.environ.get("PORT", 5000))
server = Server(host="0.0.0.0", port=port)

# Gerenciamento de login e do usuário logado
lm = LoginManager(app)


# adiciona as tabelas, formulários e controller default da aplicação
from app.models import tables, forms
from app.controllers import default
from app import scraping_infojobs
