import requests
import allure
from urls import Urls


@allure.step('Создание курьера с логином "{login}"')
def create_courier(login: str, password: str, firstname: str):
    """Отправляет запрос на создание курьера."""
    payload = {
        "login": login,
        "password": password,
        "firstName": firstname
    }
    return requests.post(Urls.URL_COURIER_CREATE, data=payload)


@allure.step('Логин курьера с логином "{login}"')
def login_courier(login: str, password: str):
    """Отправляет запрос на аутентификацию курьера."""
    payload = {
        "login": login,
        "password": password
    }
    return requests.post(Urls.URL_COURIER_LOGIN, data=payload)


@allure.step('Удаление курьера по ID {courier_id}')
def delete_courier(courier_id: int):
    """Отправляет запрос на удаление курьера по его идентификатору."""
    return requests.delete(f"{Urls.URL_BASIC}/{courier_id}")