import re
from datetime import datetime, timedelta

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    TimeField,
    DecimalField,
    SelectMultipleField,
    RadioField,
    SelectField,
)
from wtforms.validators import DataRequired, ValidationError, Optional
import sqlalchemy as sa


from app import db
from app.models import User


def get_time_choices(start_hour=0, start_minute=0, end_hour=23, end_minute=59):
    now = datetime.now()
    start = datetime(now.year, now.month, now.day, start_hour, start_minute)
    end = datetime(now.year, now.month, now.day, end_hour, end_minute)
    intervals = []
    while start < end:
        str_interval = " - ".join([start.strftime("%H:%M"), (start + timedelta(minutes=30)).strftime("%H:%M")])
        interval = ((start.strftime('%H:%M')),
                    str_interval)
        if interval[0] > (now + timedelta(minutes=30)).strftime('%H:%M'):
            intervals.append(interval)
        start = start + timedelta(minutes=30)
    return intervals


class RegistrationForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
    phone = StringField("phone", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])

    def validate_password(self, field):
        # Проверка на все параметры (длина, спец символы и тп)
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
            field.data,
        ):
            raise ValidationError("Unvalid password")

    def validate_phone(self, field):
        # Проверка на все параметры телефона
        if not re.match(r"^\+?[1-9][0-9]\d{9,14}$", field.data):
            raise ValidationError("Unvailde phone")

        user = db.session.scalar(
            sa.select(User).where(User.phone == field.data)
        )

        if user is not None:
            raise ValidationError("Please use a different phone number.")

    def validate_email(self, field):
        # Проверяем, соответствует ли адрес электронной почты требованиям
        if not re.match(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", field.data
        ):
            raise ValidationError("Unvailde email")
        # Проверка на наличие пользователя в бд
        user = db.session.scalar(
            sa.select(User).where(User.email == field.data)
        )

        if user is not None:
            raise ValidationError("Please use a different email address.")


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class PayCartForm(FlaskForm):
    payment_method = RadioField("Способ оплаты", choices=[("card", "Картой курьеру"), ("cash", "Наличными курьеру")])
    address = StringField("Адрес доставки", validators=[DataRequired()])
    entrance = StringField("Подъезд", validators=[Optional()])
    door_code = StringField("Код двери", validators=[Optional()])
    floor = StringField("Этаж", validators=[Optional()])
    apartment = StringField("Квартира", validators=[Optional()])
    time = SelectField("Время доставки", choices=get_time_choices())
    comment = TextAreaField("Комментарий", validators=[Optional()])
    submit = SubmitField("Подтвердить")

    
class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = DecimalField("Price", validators=[DataRequired()])
    ingridients = TextAreaField("Ingridients", validators=[DataRequired()])
    size = StringField("Size", validators=[DataRequired()])
    mass = StringField("Mass", validators=[DataRequired()])
    image_url = TextAreaField("Image", validators=[DataRequired()])


class EditForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    phone = StringField("Телефон", validators=[DataRequired()])
    name = StringField("Имя", validators=[DataRequired()])

    def validate_password(self, field):
        # Проверка на все параметры (длина, спец символы и тп)
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
            field.data,
        ):
            raise ValidationError("Unvalid password")

    def validate_phone(self, field):
        # Проверка на все параметры телефона
        if not re.match(r"^\+?[1-9][0-9]\d{9,14}$", field.data):
            raise ValidationError("Unvailde phone")
        user = db.session.scalar(
            sa.select(User).where(User.phone == field.data)
        )
        if user is not None:
            raise ValidationError("Please use a different phone number.")

    def validate_email(self, field):
        # Проверяем, соответствует ли адрес электронной почты требованиям
        if not re.match(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", field.data
        ):
            raise ValidationError("Unvalid email")
        # Проверка на наличие пользователя в бд
        user = db.session.scalar(
            sa.select(User).where(User.email == field.data)
        )
        if user is not None:
            raise ValidationError("Please use a different email address.")
            

class ExtraIngredientsForm(FlaskForm):
    ingredients = SelectMultipleField("ингредиенты")
    submit = SubmitField("Подтвердить")

