from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import re


class Form(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(Form):
    phone = StringField("phone", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])

    def validate_password(self, field):
        print(field.data)
        if not (
            re.match(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$",
                field.data,
            )
        ):
            raise ValidationError("Unvailde password")

    def validate_phone(self, field):
        if not re.match(r"^\+?[1-9][0-9]\d{9,14}$", field.data):
            raise ValidationError("Unvailde phone")

    def validate_email(self, field):
        if not re.match(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", field.data
        ):
            raise ValidationError("Unvailde email")
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("Please use a different email address.")


class LoginForm(Form):
    # Реализовать проверку есть ли такой пользователь в бд
    pass
