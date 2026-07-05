import requests
import allure
import pytest
from data import Data
from urls import Urls
from helpers import create_random_login, create_random_password, create_random_firstname



class TestCourierCreate:

    @allure.title('Проверка успешного создания аккаунта курьера с валидными данными')
    @allure.description('Happy path. Проверяются код и тело ответа.')
    def test_create_courier_account_success(self):
        payload = {
            'login': create_random_login(),
            'password': create_random_password(),
            'firstName': create_random_firstname()
        }
        response = requests.post(Urls.URL_COURIER_CREATE, data=payload)
        assert response.status_code == 201 and response.json() == {'ok': True}

    @allure.title('Проверка получения ошибки при повторном использовании логина для создания курьера')
    @allure.description('Проверяется только статус-код ответа.')
    def test_create_courier_account_login_taken_conflict(self, create_courier):
        login, password, firstname = create_courier  # курьер уже создан в фикстуре

        with allure.step('Попытка создать второго курьера с тем же логином'):
            second_response = create_courier(login, password, firstname)
        
        assert second_response.status_code == 409, \
            "Повторное создание с тем же логином должно вернуть 409"
    @allure.title('Проверка получения ошибки при создании курьера с незаполненными обязательными полями')
    @allure.description('В тест по очереди передаются наборы данных с пустым логином или паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('empty_credentials', [
        {'login': '', 'password': create_random_password(), 'firstName': create_random_firstname()},
        {'login': create_random_login(), 'password': '', 'firstName': create_random_firstname()}
    ])
    def test_create_courier_account_with_empty_required_fields(self, empty_credentials):
        response = requests.post(Urls.URL_COURIER_CREATE, data=empty_credentials)
        assert response.status_code == 400 and response.json() == {'message': 'Недостаточно данных для создания '
                                                                              'учетной записи'}
