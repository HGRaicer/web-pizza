import re


class User:
    def __init__(self, name: str, phone: str, password: str):
        self.name = name
        self.phone = phone
        self.password = hash(password)

    @staticmethod
    def valid_phone(phone: str)-> bool:
        return re.match(r'^\+?[1-9][0-9]\d{9,14}$', phone)


    @staticmethod
    def valid_password(password: str)-> bool:
        return re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,25}$', password)


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