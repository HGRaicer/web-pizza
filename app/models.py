from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    email: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True)
    role: so.Mapped[str] = so.mapped_column(sa.String(50), default="user")
    phone: so.Mapped[str] = so.mapped_column(sa.String(15), unique=True)
    password: so.Mapped[str] = so.mapped_column(sa.String(165))

    posts: so.WriteOnlyMapped["Order"] = so.relationship(back_populates="author", passive_deletes=True)

    def hash_password(self, password):
        self.password = generate_password_hash(password)  # мб str(password)?

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Модель продуктов для бд
class Products(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    price: so.Mapped[int] = so.mapped_column()
    ingridients: so.Mapped[str] = so.mapped_column(sa.String(150))
    size: so.Mapped[str] = so.mapped_column(sa.String(50))
    mass: so.Mapped[str] = so.mapped_column(sa.String(100))


# Модель заказов для бд
class Order(db.Model):
    id_order: so.Mapped[int] = so.mapped_column(primary_key=True)
    time: so.Mapped[str] = so.mapped_column(sa.String(100))
    check: so.Mapped[str] = so.mapped_column(sa.String(100))
    status: so.Mapped[str] = so.mapped_column(sa.String(100))
    id_person: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    address: so.Mapped[str] = so.mapped_column(sa.String(100))
    comment: so.Mapped[str] = so.mapped_column(sa.String(200))

    author: so.Mapped[User] = so.relationship(back_populates="posts")

    @staticmethod
    def count_time(time):
        now = datetime.now()
        time = " ".join([now.strftime("%Y-%m-%d"), time])
        ans = db.session.query(Order).filter(Order.time == time).count()
        return ans



@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


