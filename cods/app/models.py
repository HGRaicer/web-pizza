import re


class User:
    def __init__(self, name: str, phone: str, password: str):
        self.name = name
        self.phone = phone
        self.password = hash(password)


class Client(User):
    def __init__(self, name: str, phone: str, password: str):
        super().__init__(name, phone, password)

    def save(self):
        pass

    @staticmethod
    def check_client(phone: str, password: str):
        pass


class Admin(User):
    def __init__(self, name: str, phone: str, password: str):
        super().__init__(name, phone, password)

    def save(self):
        pass

    @staticmethod
    def check_admin(phone: str, password: str):
        pass