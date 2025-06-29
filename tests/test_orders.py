"""Тесты заказов"""

import pytest
import allure
from data.test_data import (
    VALID_ORDER_DATA, EMPTY_ORDER_DATA, INVALID_ORDER_DATA_WRONG_HASH,
    EXPECTED_RESPONSES
)
from config import Config

@allure.epic("Заказы")
class TestOrders:
    
    @allure.feature("Создание заказа")
    @allure.story("Создание заказа с авторизацией")
    @allure.title("Создание заказа авторизованным пользователем с ингредиентами")
    def test_create_order_with_auth_success(self, authorized_user, available_ingredients):
        """Тест успешного создания заказа авторизованным пользователем"""
        api_client = authorized_user["api_client"]
        
        with allure.step("Подготовка данных заказа с валидными ингредиентами"):
            if available_ingredients:
                # Берем первые два ингредиента для заказа
                ingredient_ids = [available_ingredients[0]["_id"], available_ingredients[1]["_id"]]
                order_data = {"ingredients": ingredient_ids}
            else:
                # Если ингредиенты недоступны, используем тестовые данные
                order_data = VALID_ORDER_DATA
        
        with allure.step("Отправка запроса на создание заказа"):
            response = api_client.create_order(order_data)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["success"], \
                f"Ожидался статус {Config.STATUS_CODES['success']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "order" in response_data, "В ответе должно быть поле order"
            assert "number" in response_data["order"], "В заказе должен быть номер"
            assert response_data["order"]["number"] is not None, "Номер заказа не должен быть пустым"
    
    @allure.feature("Создание заказа")
    @allure.story("Создание заказа без авторизации")
    @allure.title("Создание заказа неавторизованным пользователем")
    def test_create_order_without_auth(self, api_client, available_ingredients):
        """Тест создания заказа без авторизации"""
        with allure.step("Подготовка данных заказа"):
            if available_ingredients:
                ingredient_ids = [available_ingredients[0]["_id"], available_ingredients[1]["_id"]]
                order_data = {"ingredients": ingredient_ids}
            else:
                order_data = VALID_ORDER_DATA
        
        with allure.step("Отправка запроса на создание заказа без авторизации"):
            response = api_client.create_order(order_data)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["success"], \
                f"Ожидался статус {Config.STATUS_CODES['success']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "order" in response_data, "В ответе должно быть поле order"
            assert "number" in response_data["order"], "В заказе должен быть номер"
    
    @allure.feature("Создание заказа")
    @allure.story("Создание заказа без ингредиентов")
    @allure.title("Создание заказа с пустым списком ингредиентов")
    def test_create_order_without_ingredients(self, authorized_user):
        """Тест создания заказа без ингредиентов"""
        api_client = authorized_user["api_client"]
        
        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            response = api_client.create_order(EMPTY_ORDER_DATA)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["bad_request"], \
                f"Ожидался статус {Config.STATUS_CODES['bad_request']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message"
            assert "ingredient" in response_data["message"].lower(), \
                "Сообщение должно содержать информацию об ингредиентах"
    
    @allure.feature("Создание заказа")
    @allure.story("Создание заказа с неверными хешами ингредиентов")
    @allure.title("Создание заказа с невалидными ID ингредиентов")
    def test_create_order_with_invalid_ingredients(self, authorized_user):
        """Тест создания заказа с неверными хешами ингредиентов"""
        api_client = authorized_user["api_client"]
        
        with allure.step("Отправка запроса на создание заказа с неверными хешами"):
            response = api_client.create_order(INVALID_ORDER_DATA_WRONG_HASH)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["internal_server_error"], \
                f"Ожидался статус {Config.STATUS_CODES['internal_server_error']}, получен {response.status_code}"
        
        with allure.step("Проверка типа ответа"):
            assert "html" in response.headers.get("content-type", "").lower(), \
                "При 500 ошибке должен возвращаться HTML"
    
    @allure.feature("Получение заказов")
    @allure.story("Получение заказов авторизованного пользователя")
    @allure.title("Получение списка заказов пользователя")
    def test_get_user_orders(self, authorized_user):
        """Тест получения заказов авторизованного пользователя"""
        api_client = authorized_user["api_client"]
        
        with allure.step("Отправка запроса на получение заказов"):
            response = api_client.get_orders()
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["success"], \
                f"Ожидался статус {Config.STATUS_CODES['success']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "orders" in response_data, "В ответе должно быть поле orders"
            assert isinstance(response_data["orders"], list), "Поле orders должно быть списком"
    
    @allure.feature("Получение заказов")
    @allure.story("Получение заказов неавторизованного пользователя")
    @allure.title("Получение списка заказов без авторизации")
    def test_get_orders_without_auth(self, api_client):
        """Тест получения заказов без авторизации"""
        with allure.step("Отправка запроса на получение заказов без авторизации"):
            response = api_client.get_orders()
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["unauthorized"], \
                f"Ожидался статус {Config.STATUS_CODES['unauthorized']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message"
    
    @allure.feature("Получение ингредиентов")
    @allure.story("Получение списка доступных ингредиентов")
    @allure.title("Получение всех ингредиентов")
    def test_get_ingredients(self, api_client):
        """Тест получения списка ингредиентов"""
        with allure.step("Отправка запроса на получение ингредиентов"):
            response = api_client.get_ingredients()
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["success"], \
                f"Ожидался статус {Config.STATUS_CODES['success']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "data" in response_data, "В ответе должно быть поле data"
            assert isinstance(response_data["data"], list), "Поле data должно быть списком"
            assert len(response_data["data"]) > 0, "Список ингредиентов не должен быть пустым"
            
            # Проверяем структуру первого ингредиента
            if response_data["data"]:
                ingredient = response_data["data"][0]
                assert "_id" in ingredient, "У ингредиента должен быть _id"
                assert "name" in ingredient, "У ингредиента должно быть name"
                assert "type" in ingredient, "У ингредиента должен быть type" 