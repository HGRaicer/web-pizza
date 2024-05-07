# Импортируем необходимые модули и функции
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import os

# Создаем экземпляр Flask приложения
app = Flask(__name__)
# Устанавливаем секретный ключ для приложения, используя переменную окружения или значение по умолчанию
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "you-will-never-guess"
# Устанавливаем URI для подключения к базе данных PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:1234@localhost:5432/Web_pizza_DB"
)
# Отключаем отслеживание изменений SQLAlchemy, что улучшает производительность
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Инициализируем SQLAlchemy с нашим приложением Flask
db = SQLAlchemy()
db.init_app(app)
# Инициализируем Migrate для работы с миграциями базы данных
migrate = Migrate(app, db)
# Инициализируем LoginManager для работы с аутентификацией пользователей
login = LoginManager(app)
login.login_view = 'login'

# Импортируем модели и представления из нашего приложения
from app import models
from app import views
