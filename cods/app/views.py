from app import app, models
from flask import request, Response, render_template, flash, redirect, url_for, session
import json
import sqlalchemy as sa
from app import db
from http import HTTPStatus
from app.forms import RegistrationForm, LoginForm
from flask_login import logout_user, current_user, login_user
from sqlalchemy import func


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.validate_on_submit():
            user = models.User(
                name=form.name.data, email=form.email.data, phone=form.phone.data
            )
            user.hash_password(form.password.data)
            user.last5_order = ''
            db.session.add(user)
            db.session.commit()
            flash("Congratulations, you are now a registered user!")
            return redirect(url_for("login"))
    return render_template("registration.html", title="Sign In", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(models.User).where(models.User.email == form.email.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("menu"))
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("menu"))


@app.route("/")
def menu():
    products = models.Products.query.all()
    return render_template("menu.html", products=products)


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.form["product_id"]
    product = models.Products.query.get(product_id)
    if "cart" not in session:
        session["cart"] = {}
    if product_id in session["cart"]:
        session["cart"][
            product_id
        ] += 1  # Увеличиваем количество продукта, если он уже в корзине
    else:
        session["cart"][product_id] = 1
    session.modified = True
    return redirect(url_for("menu"))


@app.route("/cart")
def cart():
    # Получаем словарь идентификаторов продуктов и их количеств в корзине
    cart_items = session.get("cart", {})

    # Получаем объекты пицц из базы данных
    products_with_counts = models.Products.query.filter(
        models.Products.id.in_(cart_items.keys())
    ).all()
    # Создаем словарь для хранения продуктов и их количества
    products_dict = {}
    total_cost = 0

    # Подсчитываем количество каждого продукта и общую стоимость
    for product in products_with_counts:
        quantity = cart_items.get(str(product.id), 0)
        products_dict[product.id] = {"product": product, "quantity": quantity}
        total_cost += (
            product.price * quantity
        )  # Добавляем стоимость продукта в общую стоимость
    return render_template("cart.html", products=products_dict, total_cost=total_cost)
