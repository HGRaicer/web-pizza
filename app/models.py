# Импортируем необходимые модули и функции
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash, check_password_hash


# Определяем модель пользователя с методами для хеширования и проверки пароля
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    email: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True)
    role: so.Mapped[str] = so.mapped_column(sa.String(50), default="user")
    phone: so.Mapped[str] = so.mapped_column(sa.String(15), unique=True)
    password: so.Mapped[str] = so.mapped_column(sa.String(300))
    last5_order: so.Mapped[str] = so.mapped_column(sa.String(100))

    posts: so.WriteOnlyMapped["Order"] = so.relationship(back_populates="author", passive_deletes=True)

    # Метод для хеширования пароля
    def hash_password(self, password):
        self.password = generate_password_hash(password)

    # Метод для проверки пароля
    def check_password(self, password):
        return check_password_hash(self.password, password)


# Определяем модель продуктов с полями для хранения информации о продукте
class Products(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    price: so.Mapped[int] = so.mapped_column()
    ingridients: so.Mapped[str] = so.mapped_column(sa.String(150))
    size: so.Mapped[str] = so.mapped_column(sa.String(50))
    mass: so.Mapped[str] = so.mapped_column(sa.String(100))


# Определяем модель заказов с полями для хранения информации о заказе
class Order(db.Model):
    id_order: so.Mapped[int] = so.mapped_column(primary_key=True)
    time: so.Mapped[str] = so.mapped_column(sa.String(100))
    check: so.Mapped[str] = so.mapped_column(sa.String(100))
    status: so.Mapped[str] = so.mapped_column(sa.String(100))
    id_person: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    address: so.Mapped[str] = so.mapped_column(sa.String(100))
    comment: so.Mapped[str] = so.mapped_column(sa.String(200))

    author: so.Mapped[User] = so.relationship(back_populates="posts")


# Функция для загрузки пользователя по его идентификатору
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
