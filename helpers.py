import allure
import random
import string
from faker import Faker

fake = Faker()
fakeRU = Faker(locale='ru_RU')


@allure.step("Генерация случайного логина")
def create_random_login():
    login = fake.text(max_nb_chars=7) + str(fake.random_int(0, 999))
    return login


@allure.step("Генерация случайного пароля")
def create_random_password():
    password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)
    return password


@allure.step("Генерация случайного имени")
def create_random_firstname():
    first_name = fakeRU.first_name()
    return first_name
