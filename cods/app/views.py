from app import app, models
from flask import request, Response, render_template, flash, redirect, url_for
import json
from http import HTTPStatus
from app.forms import RegistrationForm, LoginForm


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.name.data, form.remember_me.data))
        return redirect(url_for('login'))
    return render_template('registration.html',  title='Sign In', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.name.data, form.remember_me.data))
        return redirect(url_for('login'))
    return render_template('login.html',  title='Sign In', form=form)