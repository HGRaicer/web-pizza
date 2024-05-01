# Импортируем необходимые модули и функции
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, TimeField
from wtforms.validators import DataRequired, ValidationError, Optional
import re
from datetime import datetime, timedelta
import sqlalchemy as sa
from app import db
from app.models import User

# Базовый класс формы с полями для электронной почты, пароля и кнопки отправки
class Form(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

# Класс формы регистрации, наследующийся от базового класса формы
class RegistrationForm(Form):
    phone = StringField("phone", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])

    # Методы для валидации пароля, телефона и электронной почты
    def validate_password(self, field):
        # Проверяем, соответствует ли пароль требованиям безопасности
        if not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
            field.data,
        ):
            raise ValidationError("Unvailde password")

    def validate_phone(self, field):
        # Проверяем, соответствует ли номер телефона требованиям
        if not re.match(r"^\+?[1-9][0-9]\d{9,14}$", field.data):
            raise ValidationError("Unvailde phone")
        user = db.session.scalar(sa.select(User).where(User.phone == field.data))
        if user is not None:
            raise ValidationError("Please use a different phone number.")

    def validate_email(self, field):
        # Проверяем, соответствует ли адрес электронной почты требованиям
        if not re.match(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", field.data
        ):
            raise ValidationError("Unvailde email")
        # Проверяем, не зарегистрирован ли уже пользователь с таким адресом электронной почты
        user = db.session.scalar(sa.select(User).where(User.email == field.data))
        if user is not None:
            raise ValidationError("Please use a different email address.")

# Класс формы входа, наследующийся от базового класса формы
class LoginForm(Form):
    pass


class PayCartForm(FlaskForm):
    number_card = StringField("Номер карты",validators=[DataRequired()])
    cvc = StringField("Код",validators=[DataRequired()])
    date = StringField("Срок",validators=[DataRequired()])
    address = TextAreaField("Адрес доставки",validators=[DataRequired()])
    time = TimeField("Время доставки", validators=[DataRequired()])
    comment = TextAreaField("Комментарий",validators=[Optional()])
    submit = SubmitField("Подтвердить")

    def validate_time(self, field):
        # Проверяем, соответствует ли время доставки требованиям
        cut_time = datetime.now()
        minimum_delivery_time = cut_time + timedelta(minutes=30)
        if field.data < minimum_delivery_time.time():
            raise ValidationError("Время доставки должно быть не ранее чем через полчаса.")
