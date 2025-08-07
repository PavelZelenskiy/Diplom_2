import requests
import allure
from ..urls import ORDERS, INGREDIENTS

@allure.feature("Работа с заказами")
class TestOrders:
    @allure.story("Создание заказа")
    @allure.title("Создание заказа с авторизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_auth(self, auth_tokens, ingredients):
        with allure.step("Подготовка данных заказа"):
            headers = {"Authorization": auth_tokens["accessToken"]}
            ingredients_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]
        
        with allure.step("Отправка запроса"):
            response = requests.post(ORDERS, json={"ingredients": ingredients_ids}, headers=headers)
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "order" in response.json()

    @allure.story("Создание заказа")
    @allure.title("Попытка создания заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_auth(self, ingredients):
        with allure.step("Подготовка данных заказа"):
            ingredients_ids = [ingredients[0]["_id"], ingredients[1]["_id"]]
        
        with allure.step("Отправка запроса без токена"):
            response = requests.post(ORDERS, json={"ingredients": ingredients_ids})
        
        with allure.step("Проверка ошибки"):
            assert response.status_code == 401
            assert response.json()["message"] == "You should be authorised"

    @allure.story("Создание заказа")
    @allure.title("Создание заказа с неверными ингредиентами")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_order_with_invalid_ingredients(self, auth_tokens):
        with allure.step("Подготовка неверных данных"):
            headers = {"Authorization": auth_tokens["accessToken"]}
            invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
        
        with allure.step("Отправка запроса"):
            response = requests.post(ORDERS, json={"ingredients": invalid_ingredients}, headers=headers)
        
        with allure.step("Проверка ошибки сервера"):
            assert response.status_code == 500

@allure.feature("Получение данных")
class TestIngredients:
    @allure.story("Работа с ингредиентами")
    @allure.title("Получение списка ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_ingredients(self):
        with allure.step("Отправка запроса"):
            response = requests.get(INGREDIENTS)
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert isinstance(response.json()["data"], list)
            assert len(response.json()["data"]) > 0