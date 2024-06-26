import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
# Устанавливаем секретный ключ для приложения, используя переменную окружения или значение по умолчанию
app.config["SECRET_KEY"] = (
    os.environ.get("SECRET_KEY") or "you-will-never-guess"
)
# Устанавливаем URI для подключения к PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or (
    "postgresql://postgres:1234@localhost:5432/web_pizza_db"
)

# Отключаем отслеживание изменений SQLAlchemy, что улучшает производительность
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(
    app, db
)  # Инициализируем для работы с миграциями базы данных
# Инициализируем LoginManager для работы с аутентификацией пользователей
login = LoginManager(app)
login.login_view = "login"


from app import models
from app import views
