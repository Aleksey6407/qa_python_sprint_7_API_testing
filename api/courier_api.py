# api/courier_api.py
import requests
from urls import Urls

def create_courier(login: str, password: str, firstname: str):
    """Создание курьера."""
    payload = {
        "login": login,
        "password": password,
        "firstName": firstname
    }
    return requests.post(Urls.URL_COURIER_CREATE, data=payload)

def login_courier(login: str, password: str):
    """Логин курьера."""
    payload = {
        "login": login,
        "password": password
    }
    return requests.post(Urls.URL_COURIER_LOGIN, data=payload)

def delete_courier(courier_id: int):
    """Удаление курьера по ID."""
    # URL должен быть шаблоном, например: URL_COURIER_DELETE = f'{URL_BASIC}api/v1/courier/{}'
    url = Urls.URL_COURIER_DELETE.format(courier_id)
    return requests.delete(url)