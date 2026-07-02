import requests
import allure
import pytest
from data import Data
from urls import Urls
from helpers import create_random_login, create_random_password, create_random_firstname


@pytest.fixture
def create_courier():
    """
    Фикстура создаёт курьера с валидными данными, возвращает его учётные данные
    и удаляет курьера после завершения теста.
    """
    # Генерируем уникальные данные для курьера
    login = create_random_login()
    password = create_random_password()
    first_name = "TestCourier"

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # 1. Создаём курьера
    create_response = requests.post(Urls.URL_COURIER_CREATE, data=payload)
    assert create_response.status_code == 201, "Не удалось создать курьера"

    # Получаем ID созданного курьера (для последующего удаления)
    courier_id = create_response.json().get("id")
    assert courier_id, "ID курьера не получен"

    # Возвращаем данные для входа
    credentials = {
        "login": login,
        "password": password
    }

    yield credentials  # передаём данные в тест

    # 2. Удаляем курьера после теста
    delete_response = requests.delete(f"{Urls.URL_COURIER_DELETE}/{courier_id}")
    # Если удаление не удалось, тест всё равно завершится, но мы можем проигнорировать ошибку
    # или добавить проверку по желанию
    assert delete_response.status_code == 200, "Не удалось удалить курьера"


class TestCourierLogin:

    @allure.title('Проверка успешной аутентификации курьера при вводе валидных данных')
    @allure.description('Happy path. Проверяются код и тело ответа. Курьер создаётся перед тестом и удаляется после.')
    def test_courier_login_success(self, create_courier):
        # Используем данные от фикстуры
        credentials = create_courier
        response = requests.post(Urls.URL_COURIER_LOGIN, data=credentials)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert 'id' in response.json(), "В ответе отсутствует 'id'"

    @allure.title('Проверка получения ошибки аутентификации курьера при вводе невалидных данных')
    @allure.description('В тест по очереди передаются наборы данных с несуществующим логином или неверным паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('nonexistent_credentials', [
        {'login': create_random_login(), 'password': create_random_password()},
        Data.courier_data_with_wrong_password
    ])
    def test_courier_login_nonexistent_data_not_found(self, nonexistent_credentials):
        response = requests.post(Urls.URL_COURIER_LOGIN, data=nonexistent_credentials)
        assert response.status_code == 404 and response.json() == {'message': 'Учетная запись не найдена'}

    @allure.title('Проверка получения ошибки аутентификации курьера с пустым полем логина или пароля')
    @allure.description('В тест по очереди передаются наборы данных с пустым логином или паролем. '
                        'Проверяются код и тело ответа.')
    @pytest.mark.parametrize('empty_credentials', [
        {'login': '', 'password': create_random_password()},
        {'login': Data.valid_login, 'password': ''}
    ])
    def test_courier_login_empty_credentials_bad_request(self, empty_credentials):
        response = requests.post(Urls.URL_COURIER_LOGIN, data=empty_credentials)
        assert response.status_code == 400 and response.json() == {'message': 'Недостаточно данных для входа'}
