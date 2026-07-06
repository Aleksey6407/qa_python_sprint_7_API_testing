import pytest
import allure
from api.courier_api import create_courier, login_courier, delete_courier
from helpers import generate_random_login, generate_random_password, generate_random_firstname


@pytest.fixture
def create_courier_fixture():
    """
    Фикстура создаёт курьера с уникальными данными.
    После теста логинится, получает ID и удаляет курьера.
    Возвращает: login, password, firstname
    """
    login = generate_random_login()
    password = generate_random_password()
    firstname = generate_random_firstname()

    with allure.step(f'Создание курьера (логин: {login})'):
        create_response = create_courier(login, password, firstname)
        # Не проверяем статус здесь - это будет в тесте

    yield login, password, firstname

    # Очистка: получаем ID через логин и удаляем
    with allure.step(f'Удаление курьера с логином {login}'):
        login_response = login_courier(login, password)
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')
            if courier_id:
                delete_courier(courier_id)