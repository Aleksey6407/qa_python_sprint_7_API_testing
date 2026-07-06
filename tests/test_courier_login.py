import allure
import pytest
from data import Data
from helpers import create_random_login, create_random_password
from api.courier_api import login_courier


class TestCourierLogin:

    @allure.title('Проверка успешной аутентификации курьера при вводе валидных данных')
    @allure.description('Happy path. Проверяются статус-код и тело ответа.')
    def test_courier_login_success(create_courier_fixture):
        login, password, _ = create_courier_fixture

        with allure.step('Логин созданного курьера'):
            response = login_courier(login, password)

        # Проверяем статус
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        
        # Проверяем, что в ответе есть id
        assert response.json().get('id') is not None, "Ответ должен содержать id курьера"
    @allure.title('Проверка получения ошибки аутентификации курьера при вводе невалидных данных')
    @allure.description('В тест по очереди передаются наборы данных с несуществующим логином или неверным паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('nonexistent_credentials', [
        {'login': create_random_login(), 'password': create_random_password()},
        Data.courier_data_with_wrong_password
    ])
    def test_courier_login_nonexistent_data_not_found(self, nonexistent_credentials):
        response = login_courier(
            nonexistent_credentials['login'],
            nonexistent_credentials['password']
        )
        assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
        assert response.json() == {'message': 'Учетная запись не найдена'}

    @allure.title('Проверка получения ошибки аутентификации курьера с пустым полем логина или пароля')
    @allure.description('В тест по очереди передаются наборы данных с пустым логином или паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('empty_credentials', [
        {'login': '', 'password': create_random_password()},
        {'login': Data.valid_login, 'password': ''}
    ])
    def test_courier_login_empty_credentials_bad_request(self, empty_credentials):
        response = login_courier(
            empty_credentials.get('login', ''),
            empty_credentials.get('password', '')
        )
        assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
        assert response.json() == {'message': 'Недостаточно данных для входа'}