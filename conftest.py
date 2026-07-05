import pytest
import allure
from api.courier_api import create_courier
from helpers import generate_random_login, generate_random_password, generate_random_firstname

@pytest.fixture
def create_courier():
    """Фикстура создаёт курьера с уникальными данными и возвращает логин, пароль и имя."""
    login = generate_random_login()
    password = generate_random_password()
    firstname = generate_random_firstname()

    with allure.step(f'Создание курьера через фикстуру (логин: {login})'):
        response = create_courier(login, password, firstname)
        assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"

    yield login, password, firstname

    # Очистка отсутствует, т.к. ID не возвращается, а удаление только по ID.
    # При желании можно добавить логирование или вызов отдельной функции очистки БД.