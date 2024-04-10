from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "you-will-never-guess"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:1234@localhost:5432/Web_pizza_DB"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import models
from app import views
