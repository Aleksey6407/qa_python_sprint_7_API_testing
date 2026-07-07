import requests
import allure
import pytest
from data import Data
from urls import Urls
from helpers import create_random_login, create_random_password, create_random_firstname
from api.courier_api import create_courier


class TestCourierCreate:

    @allure.title('Проверка создания курьера с валидными данными')
    @allure.description('Проверяется успешное создание курьера.')
    def test_create_courier_account_success(self, create_courier_fixture):
        login, password, firstname = create_courier_fixture
        # Фикстура уже создала курьера, проверяем что он существует
        # Можно добавить проверку через логин
        response = create_courier(login, password, firstname)
        # Так как курьер уже создан, ожидаем конфликт
        assert response.status_code == 409


    @allure.title('Проверка получения ошибки при повторном использовании логина для создания курьера')
    @allure.description('Проверяются статус-код и тело ответа.')
    def test_create_courier_account_login_taken_conflict(self, create_courier_fixture):
        login, password, firstname = create_courier_fixture

        with allure.step('Попытка создать второго курьера с тем же логином'):
            second_response = create_courier(login, password, firstname)

        # Проверяем статус
        assert second_response.status_code == 409, \
            "Повторное создание с тем же логином должно вернуть 409"
        
        # Проверяем тело ответа
        error_message = second_response.json().get('message')
        assert error_message == "Этот логин уже используется. Попробуйте другой.", \
            f"Ожидалось сообщение 'Этот логин уже используется. Попробуйте другой.', получено: {error_message}"


    @allure.title('Проверка создания курьера с пустыми обязательными полями (login и password)')
    @allure.description('Проверяется код и тело ответа. firstName - необязательное поле, поэтому не проверяется.')
    def test_create_courier_account_with_empty_required_fields(self, empty_credentials):
        response = create_courier(
            empty_credentials.get('login', ''),
            empty_credentials.get('password', ''),
            'TestName'  # передаём любое значение для firstName
        )
        assert response.status_code == 400
        # Проверяем только message, без code
        assert response.json().get('message') == 'Недостаточно данных для создания учетной записи'
