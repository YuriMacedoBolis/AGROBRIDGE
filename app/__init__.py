from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
app = Flask(__name__)

#CONFIGURAÇÕES DO APP
app.config["SECRET_KEY"] = 'Escola21'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agrobridge.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app ,db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


from app import routes , models