from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '8639f43b71b224ad036d1047322a6b39'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nysc.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from nyscforum import routes