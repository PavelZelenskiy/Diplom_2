import pytest
import requests
import allure
from .helpers import generate_user_data
from .urls import AUTH_REGISTER, AUTH_LOGIN, INGREDIENTS

@pytest.fixture
def registered_user():
    with allure.step("Регистрация тестового пользователя"):
        user_data = generate_user_data()
        response = requests.post(AUTH_REGISTER, json=user_data)
        yield user_data

@pytest.fixture
def auth_tokens(registered_user):
    with allure.step("Авторизация пользователя и получение токенов"):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = requests.post(AUTH_LOGIN, json=login_data)
        return {
            "accessToken": response.json()["accessToken"],
            "refreshToken": response.json()["refreshToken"]
        }

@pytest.fixture
def ingredients():
    with allure.step("Получение списка ингредиентов"):
        response = requests.get(INGREDIENTS)
        return response.json()["data"]