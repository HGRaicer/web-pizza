from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    email: so.Mapped[str] = so.mapped_column(sa.String(100), unique = True)
    phone: so.Mapped[str] = so.mapped_column(sa.String(15), unique = True)
    password: so.Mapped[str] = so.mapped_column(sa.String(30))
    last5_order: so.Mapped[str] = so.mapped_column(sa.String(100))

    posts: so.WriteOnlyMapped['Order'] = so.relationship(back_populates='author')


class Admin(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    password: so.Mapped[str] = so.mapped_column(sa.String(30))
    position: so.Mapped[str] = so.mapped_column(sa.String(50))
    email: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True)


class Products(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    price: so.Mapped[int] = so.mapped_column()
    ingridients: so.Mapped[str] = so.mapped_column(sa.String(150))
    size: so.Mapped[str] = so.mapped_column(sa.String(50))
    mass: so.Mapped[str] = so.mapped_column(sa.String(100))


class Order(db.Model):
    id_order: so.Mapped[int] = so.mapped_column(primary_key=True)
    time: so.Mapped[str] = so.mapped_column(sa.String(100))
    check: so.Mapped[str] = so.mapped_column(sa.String(100))
    status: so.Mapped[str] = so.mapped_column(sa.String(100))
    id_person: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    addres: so.Mapped[str] = so.mapped_column(sa.String(100))
    comment: so.Mapped[str] = so.mapped_column(sa.String(200))

    author: so.Mapped[User] = so.relationship(back_populates='posts')