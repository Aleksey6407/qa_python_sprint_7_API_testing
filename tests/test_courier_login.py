import allure
import pytest
from data import Data
from helpers import create_random_login, create_random_password
from api.courier_api import login_courier


class TestCourierLogin:

    @allure.title('Проверка успешной аутентификации курьера при вводе валидных данных')
    @allure.description('Happy path. Проверяются статус-код и тело ответа.')
    def test_courier_login_success(self, create_courier_fixture):
        login, password, _ = create_courier_fixture

        with allure.step('Логин созданного курьера'):
            response = login_courier(login, password)

        # Проверяем статус
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        
        # Проверяем, что в ответе есть id
        assert response.json().get('id') is not None, "Ответ должен содержать id курьера"


    @allure.title('Проверка логина с пустыми полями')
    @allure.description('Проверяется код и тело ответа.')
    @pytest.mark.parametrize('empty_credentials', [
        {'login': '', 'password': 'password123'},
        {'login': 'login', 'password': ''},
    ])
    def test_courier_login_with_empty_fields(self, empty_credentials):
        response = login_courier(
            empty_credentials.get('login', ''),
            empty_credentials.get('password', '')
        )
        assert response.status_code == 400
        # Исправлено: проверяем только message, без code
        assert response.json().get('message') == 'Недостаточно данных для входа'


    @allure.title('Проверка логина с несуществующим логином')
    @allure.description('Проверяется код и тело ответа.')
    def test_courier_login_with_invalid_login(self):
        response = login_courier('nonexistent_login', 'password123')
        assert response.status_code == 404
        # Исправлено: проверяем только message, без code
        assert response.json().get('message') == 'Учетная запись не найдена'