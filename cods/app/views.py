from app import app, models
from flask import request, Response
import json
from http import HTTPStatus


@app.post('/client/registration')
def clinet_registration():
    data = json.loads(request.data)
    if (not models.User.valid_phone(data['phone'])) or (not models.User.valid_password(data['password'])):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.Client(name=data['name'], phone=data['phone'], password=data['password'])
    user.save()
    return Response(status=HTTPStatus.CREATED) #сделать переход на страницу с меню


@app.post('/admin/registration')
def admin_registration():
    data = json.loads(request.data)
    if not models.User.valid_phone(data['phone']) or not models.User.valid_password(data['password']):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.Admin(name=data['name'], phone=data['phone'], password=data['password'])
    user.save()
    return Response(status=HTTPStatus.CREATED) #сделать переход на главную страницу

@app.post('/client/login')
def client_login():
    data = json.loads(request.data)
    if not models.Client.check_client(data['phone'], data['password']):
        return Response(status=HTTPStatus.BAD_REQUEST)

    return Response(status=HTTPStatus.OK) #сделать переход на страницу с меню


@app.post('/admin/login')
def admin_login():
    data = json.loads(request.data)
    if not models.Admin.check_admin(data['phone'], data['password']):
        return Response(status=HTTPStatus.BAD_REQUEST)

    return Response(status=HTTPStatus.OK)  # сделать переход на главную страницу