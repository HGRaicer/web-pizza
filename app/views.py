from datetime import datetime
from functools import wraps
from urllib.parse import urlsplit

from flask import request, render_template, flash, redirect, url_for, session, jsonify
import sqlalchemy as sa
from flask_login import logout_user, current_user, login_user, login_required


from app import app, models
from app import db
from app.forms import RegistrationForm, LoginForm, PayCartForm, ProductForm
from app.forms import get_time_choices



@app.route("/registration", methods=["GET", "POST"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User()
        user.phone = form.phone.data
        user.email = form.email.data
        user.name = form.name.data
        user.hash_password(form.password.data)
        user.last5_order = ''
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")

        return redirect(url_for("login"))
    # Возвращаем шаблон страницы регистрации с формой
    return render_template("registration.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("menu"))
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
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('menu')
        return redirect(next_page)
    # Возвращаем шаблон страницы входа с формой
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("menu"))


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
    is_empty = True
    # Проверяем, есть ли в сессии корзина
    if "cart" not in session or len(session["cart"]) == 0:
        is_empty = False
        return render_template("cart.html", is_empty=is_empty)
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
@login_required
@app.route("/pay_cart", methods=["GET", "POST"])
def pay_cart():
    if current_user.is_authenticated:
        form = PayCartForm()
        intervals = get_time_choices()
        form.time.choices = intervals
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
            # Получение текущего времени заказа
            now = datetime.now()
            time = " ".join([now.strftime("%Y-%m-%d"), form.time.data])


            # Сохраняем информацию о заказе
            order = models.Order(
                id_person=current_user.id,
                address=form.address.data,
                status="Принято",
                comment=form.comment.data,
                check=check,
                time=time
            )
            # Очищаем корзину
            session["cart"].clear()
            db.session.add(order)
            db.session.commit()
            session["order"] = order.id_order
            return redirect(url_for("order_tracking"))
        return render_template("pay_cart.html", form=form, title="Pay_cart")
    else:
        return redirect(url_for("login"))

@app.route('/get_delivery_times', methods=['POST'])
def get_delivery_times():
    time = request.form['time']
    count_order = models.Order.count_time(time)
    if count_order < 10:
        return jsonify({'delivery_time': 'Низкая нагруженность'})
    if count_order < 50:
        return jsonify({'delivery_time': 'Средняя нагруженность'})
    return jsonify({'delivery_time': 'Высокая нагруженность'})



@app.route("/order_tracking", methods=["GET"])
def order_tracking():
    id_order = session.get("order")
    if models.Order.query.get(id_order) is None:
        return redirect(url_for("menu"))
    status_order = models.Order.query.get(id_order).status
    return render_template("order_tracking.html", status_order=status_order)


@app.route("/get_order_status", methods=["GET"])
def get_order_status():
    id_order = session.get("order")
    if models.Order.query.get(id_order) is None:
        return jsonify({"status": "Заказа не существует"})
    status_order = models.Order.query.get(id_order).status
    return jsonify({"status": status_order})


# Admin page
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'),)
        if current_user.role != 'admin':
            return redirect(url_for('menu'))
        return func(*args, **kwargs)
    return decorated_view


@app.route('/admin')
@login_required
@admin_required
def admin():
    return redirect(url_for('admin_users'))


@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = models.User.query.all()
    return render_template('admin_users.html', users=users)


@app.route('/admin/users/change_role/<int:user_id>/<new_role>', methods=['GET'])
@login_required
@admin_required
def change_user_role(user_id, new_role):
    user = models.User.query.get_or_404(user_id)
    user.role = new_role
    db.session.commit()

    return redirect(url_for('admin_users'))


@app.route('/admin/products')
@login_required
@admin_required
def admin_products():
    products = models.Products.query.all()
    return render_template('admin_products.html', products=products)


@app.route('/admin/orders')
@login_required
@admin_required
def admin_orders():
    orders = models.Order.query.all()
    return render_template('admin_orders.html', orders=orders)


@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = models.Products(name=form.name.data, price=form.price.data,
                                      ingridients=form.ingridients.data, size=form.size.data,
                                      mass=form.mass.data)

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('admin_products'))
    return render_template('add_product.html', form=form)


@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = models.Products.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        return redirect(url_for('admin_products'))
    return render_template('edit_product.html', form=form, product_id=product_id)


@app.route('/admin/orders/update_status/<int:order_id>/<new_status>', methods=['GET'])
@login_required
@admin_required
def update_order_status(order_id, new_status):
    order = models.Order.query.get_or_404(order_id)
    order.status = new_status
    db.session.commit()

    return redirect(url_for('admin_orders'))


@app.route('/admin/users/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = models.User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('admin_users'))


@app.route('/admin/orders/delete/<int:order_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_order(order_id):
    order = models.Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()

    return redirect(url_for('admin_orders'))


@app.route('/admin/products/delete/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = models.Products.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('admin_products'))


@login_required
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if current_user.is_authenticated:
        orders = models.Order.query.filter(models.Order.id_person == current_user.id).all()
        return render_template("profile.html", title="Your profile", orders=orders)