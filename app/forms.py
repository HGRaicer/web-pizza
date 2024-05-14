from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, TimeField, DecimalField
from wtforms.validators import DataRequired, ValidationError, Optional
import re
from datetime import datetime, timedelta
import sqlalchemy as sa
from app import db
from app.models import User


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
                field.data, ):
            raise ValidationError("Unvalid password")

    def validate_phone(self, field):
        # Проверка на все параметры телефона
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
        # Проверка на наличие пользователя в бд
        user = db.session.scalar(sa.select(User).where(User.email == field.data))
        if user is not None:
            raise ValidationError("Please use a different email address.")


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class PayCartForm(FlaskForm):
    number_card = StringField("Номер карты", validators=[DataRequired()])
    cvc = StringField("Код", validators=[DataRequired()])
    date = StringField("Срок", validators=[DataRequired()])
    address = TextAreaField("Адрес доставки", validators=[DataRequired()])
    time = TimeField("Время доставки", validators=[DataRequired()])
    comment = TextAreaField("Комментарий", validators=[Optional()])
    submit = SubmitField("Подтвердить")

    def validate_time(self, field):
        # Проверяем, соответствует ли время доставки требованиям
        cut_time = datetime.now()
        minimum_delivery_time = cut_time + timedelta(minutes=30)
        if field.data < minimum_delivery_time.time():
            raise ValidationError("Время доставки должно быть не ранее чем через полчаса.")


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    ingridients = TextAreaField("Ingridients", validators=[DataRequired()])
    size = StringField("Size", validators=[DataRequired()])
    mass = StringField("Mass", validators=[DataRequired()])
# image = TextAreaField("Image", validators=[DataRequired()])
