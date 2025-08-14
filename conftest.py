import pytest
import requests
import allure
from .helpers import generate_user_data
from .urls import AUTH_REGISTER, AUTH_LOGIN, INGREDIENTS, USER

@pytest.fixture
def registered_user():
    with allure.step("Регистрация тестового пользователя"):
        user_data = generate_user_data()
        response = requests.post(AUTH_REGISTER, json=user_data)

        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        login_response = requests.post(AUTH_LOGIN, json=login_data)

        access_token = login_response.json()["accessToken"]
        user_data["accessToken"] = access_token

        yield user_data

        with allure.step("Удаление тестового пользователя"):
            headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
        }
        delete_response = requests.delete(USER, headers=headers)

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