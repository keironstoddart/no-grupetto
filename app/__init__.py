from flask import Flask
app = Flask(__name__)
app.config.from_object('config')

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_login import LoginManager
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models
