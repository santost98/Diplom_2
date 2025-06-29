"""Тестовые данные для API тестов Stellar Burgers"""

# Данные для регистрации пользователя
VALID_USER_DATA = {
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
}

INVALID_USER_DATA_MISSING_EMAIL = {
    "password": "password123",
    "name": "Test User"
}

INVALID_USER_DATA_MISSING_PASSWORD = {
    "email": "test@example.com",
    "name": "Test User"
}

INVALID_USER_DATA_MISSING_NAME = {
    "email": "test@example.com",
    "password": "password123"
}

# Данные для логина
VALID_LOGIN_DATA = {
    "email": "test@example.com",
    "password": "password123"
}

INVALID_LOGIN_DATA_WRONG_PASSWORD = {
    "email": "test@example.com",
    "password": "wrongpassword"
}

INVALID_LOGIN_DATA_WRONG_EMAIL = {
    "email": "wrong@example.com",
    "password": "password123"
}

# Данные для заказов
VALID_ORDER_DATA = {
    "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6e"]
}

EMPTY_ORDER_DATA = {
    "ingredients": []
}

INVALID_ORDER_DATA_WRONG_HASH = {
    "ingredients": ["invalid_hash_1", "invalid_hash_2"]
}

# Ожидаемые ответы
EXPECTED_RESPONSES = {
    "user_created": {
        "success": True,
        "user": {
            "email": "test@example.com",
            "name": "Test User"
        }
    },
    
    "user_already_exists": {
        "success": False,
        "message": "User already exists"
    },
    
    "missing_field": {
        "success": False,
        "message": "Email, password and name are required fields"
    },
    
    "login_success": {
        "success": True,
        "user": {
            "email": "test@example.com",
            "name": "Test User"
        }
    },
    
    "login_failed": {
        "success": False,
        "message": "email or password are incorrect"
    },
    
    "order_created": {
        "success": True,
        "order": {
            "number": None  # Будет заполнено динамически
        }
    },
    
    "order_no_ingredients": {
        "success": False,
        "message": "Ingredient ids must be provided"
    },
    
    "order_invalid_ingredients": {
        "success": False,
        "message": "Internal Server Error"
    }
} 