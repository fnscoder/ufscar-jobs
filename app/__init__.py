import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server())

port = int(os.environ.get("PORT", 5000))

server = Server(host="0.0.0.0", port=port)

lm = LoginManager(app)


from app.models import tables, forms
from app.controllers import default
