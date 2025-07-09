import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Конфигурация для API тестов Stellar Burgers"""
    
    # Базовый URL API
    BASE_URL = "https://stellarburgers.nomoreparties.site"
    
    # Эндпоинты API
    ENDPOINTS = {
        "register": "/api/auth/register",
        "login": "/api/auth/login", 
        "user": "/api/auth/user",
        "orders": "/api/orders",
        "ingredients": "/api/ingredients"
    }
    
    # Тестовые данные
    TEST_DATA = {
        "valid_email": "test@example.com",
        "valid_password": "password123",
        "valid_name": "Test User"
    }
    
    # Ожидаемые статус коды
    STATUS_CODES = {
        "success": 200,
        "created": 201,
        "bad_request": 400,
        "unauthorized": 401,
        "forbidden": 403,
        "not_found": 404,
        "conflict": 409,
        "internal_server_error": 500
    } 