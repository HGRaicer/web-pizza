# Импортируем необходимые модули и функции
from app import app, models
from flask import request, Response, render_template, flash, redirect, url_for, session
import json
import sqlalchemy as sa
from app import db
from http import HTTPStatus
from app.forms import RegistrationForm, LoginForm, PayCartForm
from flask_login import logout_user, current_user, login_user
from sqlalchemy import func
import time
import ast

# Маршрут для регистрации нового пользователя
@app.route("/registration", methods=["GET", "POST"])
def registration():
    # Если пользователь уже авторизован, перенаправляем его на главную страницу
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    # Создаем форму регистрации
    form = RegistrationForm()
    # Проверяем, отправлена ли форма и валидна ли она
    if form.validate_on_submit():
        # Создаем нового пользователя с данными из формы
        user = models.User(
            name=form.name.data, email=form.email.data, phone=form.phone.data
        )
        # Хешируем пароль пользователя
        user.hash_password(form.password.data)
        # Устанавливаем начальное значение последних 5 заказов
        user.last5_order = ''
        # Добавляем пользователя в базу данных и сохраняем изменения
        db.session.add(user)
        db.session.commit()
        # Выводим сообщение об успешной регистрации
        flash("Congratulations, you are now a registered user!")
        # Перенаправляем пользователя на страницу входа
        return redirect(url_for("login"))
    # Возвращаем шаблон страницы регистрации с формой
    return render_template("registration.html", title="Sign In", form=form)

# Маршрут для входа в систему
@app.route("/login", methods=["GET", "POST"])
def login():
    # Если пользователь уже авторизован, перенаправляем его на главное меню
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
    # Создаем форму входа
    form = LoginForm()
    # Проверяем, отправлена ли форма и валидна ли она
    if form.validate_on_submit():
        # Ищем пользователя по электронной почте
        user = db.session.scalar(
            sa.select(models.User).where(models.User.email == form.email.data)
        )
        # Проверяем, существует ли пользователь и правильно ли введен пароль
        if user is None or not user.check_password(form.password.data):
            # Выводим сообщение об ошибке
            flash("Invalid username or password")
            return redirect(url_for("login"))
        # Авторизуем пользователя
        login_user(user, remember=form.remember_me.data)
        # Перенаправляем пользователя на главное меню
        return redirect(url_for("menu"))
    # Возвращаем шаблон страницы входа с формой
    return render_template("login.html", title="Sign In", form=form)

# Маршрут для выхода из системы
@app.route("/logout")
def logout():
    # Выход из системы
    logout_user()
    # Перенаправляем пользователя на главное меню
    return redirect(url_for("menu"))

# Маршрут для главного меню
@app.route("/")
def menu():
    # Получаем список всех продуктов
    products = models.Products.query.all()
    # Возвращаем шаблон главного меню с продуктами
    return render_template("menu.html", products=products)

# Маршрут для добавления товара в корзину
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    # Получаем идентификатор товара из формы
    product_id = request.form["product_id"]
    # Получаем товар по идентификатору
    product = models.Products.query.get(product_id)
    # Если корзина еще не создана, создаем ее
    if "cart" not in session:
        session["cart"] = {}
    # Если товар уже в корзине, увеличиваем количество
    if product_id in session["cart"]:
        session["cart"][product_id] += 1
    else:
        # Добавляем товар в корзину
        session["cart"][product_id] = 1
    # Обновляем сессию
    session.modified = True
    # Перенаправляем пользователя на главное меню
    return redirect(url_for("menu"))

# Маршрут для просмотра корзины
@app.route("/cart")
def cart():
    # Получаем словарь идентификаторов товаров и их количеств в корзине
    cart_items = session.get("cart", {})
    # Получаем товары из базы данных по идентификаторам в корзине
    products_with_counts = models.Products.query.filter(
        models.Products.id.in_(cart_items.keys())
    ).all()
    # Создаем словарь для хранения товаров и их количества
    products_dict = {}
    total_cost = 0
    # Подсчитываем общую стоимость товаров в корзине
    for product in products_with_counts:
        quantity = cart_items.get(str(product.id), 0)
        products_dict[product.id] = {"product": product, "quantity": quantity}
        total_cost += product.price * quantity
    # Возвращаем шаблон корзины с товарами и их количеством
    return render_template("cart.html", products=products_dict, total_cost=total_cost)


# Маршрут для удаления товара из корзины
@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    # Получаем идентификатор товара из формы
    product_id = request.form["product_id"]
    # Удаляем товар из корзины
    if product_id in session["cart"]:
        del session["cart"][product_id]
    # Обновляем сессию
    session.modified = True
    # Перенаправляем пользователя в корзину
    return redirect(url_for("cart"))


# Маршрут для уменьшения количества товара в корзине
@app.route("/decrease_quantity_cart", methods=["POST"])
def decrease_quantity_cart():
    # Получаем идентификатор товара из формы
    product_id = request.form["product_id"]
    # Уменьшаем количество товара в корзине
    if product_id in session["cart"]:
        session["cart"][product_id] -= 1
        if session["cart"][product_id] == 0:
            del session["cart"][product_id]
    # Обновляем сессию
    session.modified = True
    # Перенаправляем пользователя в корзину
    return redirect(url_for("cart"))


# Маршрут для увеличения количества товара в корзине
@app.route("/increase_quantity_cart", methods=["POST"])
def increase_quantity_cart():
    # Получаем идентификатор товара из формы
    product_id = request.form["product_id"]
    # Увеличиваем количество товара в корзине
    if product_id in session["cart"]:
        session["cart"][product_id] += 1
    # Обновляем сессию
    session.modified = True
    # Перенаправляем пользователя в корзину
    return redirect(url_for("cart"))


# Маршрут для оплаты корзины
@app.route("/pay_cart", methods=["GET", "POST"])
def pay_cart():
    if current_user.is_authenticated:
        form = PayCartForm()
        if form.validate_on_submit():
            # Получаем словарь идентификаторов товаров и их количеств в корзине
            cart_items = session.get("cart", {})
            products = ''
            total_cost = 0
            # формируем строчку для чека вида id продукта:количество| и подсчитываем общую сумму
            for id_product, quantity in cart_items.items():
                products = products + f'{id_product}:{quantity}|'
                total_cost += models.Products.query.get(id_product).price * quantity
            # формируем чек
            check = f"{total_cost}|" + products
            # подгружаем время в которое сделан заказ
            named_tuple = time.localtime()  # получить struct_time
            # преобразует в понятный вид для чтения - день/месяц/год, час:минута:секунда
            time_string = time.strftime("%d/%m/%Y, %H:%M:%S", named_tuple)
            # Сохраняем информацию о заказе
            order = models.Order(
                id_person=current_user.id,
                address=form.address.data,
                status="Принято",
                comment=form.comment.data,
                check=check,
                time=time_string
            )
            # Очищаем корзину
            session.clear()
            db.session.add(order)
            db.session.commit()
            return redirect(url_for("menu"))
        return render_template("pay_cart.html", title="Pay_cart", form=form)
    else:
        return redirect(url_for("login"))