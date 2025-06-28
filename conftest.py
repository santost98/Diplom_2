"""Фикстуры для тестов API Stellar Burgers"""

import pytest
import allure
from helpers.api_client import StellarBurgersAPI
from helpers.user_generator import UserGenerator

@pytest.fixture
def api_client():
    """Фикстура для создания API клиента"""
    return StellarBurgersAPI()

@pytest.fixture
def unique_user_data():
    """Фикстура для генерации уникальных данных пользователя"""
    return UserGenerator.generate_unique_user_data()

@pytest.fixture
def registered_user(api_client, unique_user_data):
    """Фикстура для создания зарегистрированного пользователя"""
    with allure.step("Регистрация пользователя"):
        response = api_client.register_user(unique_user_data)
        assert response.status_code == 200, f"Ошибка регистрации: {response.text}"
        
        # Получаем токен из ответа
        response_data = response.json()
        if response_data.get("success") and "accessToken" in response_data:
            api_client.set_access_token(response_data["accessToken"])
        
        return {
            "user_data": unique_user_data,
            "api_client": api_client,
            "access_token": response_data.get("accessToken")
        }

@pytest.fixture
def authorized_user(unique_user_data):
    """Фикстура для создания авторизованного пользователя"""
    api_client = StellarBurgersAPI()
    
    with allure.step("Регистрация пользователя"):
        response = api_client.register_user(unique_user_data)
        assert response.status_code == 200, f"Ошибка регистрации: {response.text}"
    
    with allure.step("Авторизация пользователя"):
        login_data = {
            "email": unique_user_data["email"],
            "password": unique_user_data["password"]
        }
        response = api_client.login_user(login_data)
        assert response.status_code == 200, f"Ошибка авторизации: {response.text}"
        
        response_data = response.json()
        if response_data.get("success") and "accessToken" in response_data:
            api_client.set_access_token(response_data["accessToken"])
        
        return {
            "user_data": unique_user_data,
            "api_client": api_client,
            "access_token": response_data.get("accessToken")
        }

@pytest.fixture
def available_ingredients(api_client):
    """Фикстура для получения доступных ингредиентов"""
    with allure.step("Получение списка ингредиентов"):
        response = api_client.get_ingredients()
        assert response.status_code == 200, f"Ошибка получения ингредиентов: {response.text}"
        
        response_data = response.json()
        if response_data.get("success") and "data" in response_data:
            return response_data["data"]
        return [] 