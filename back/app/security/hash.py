# app/security/hash.py
from passlib.context import CryptContext

# Простая рабочая конфигурация - используем только bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Хэширует пароль с учетом ограничения bcrypt (72 байта).
    """
    # Проверяем длину пароля
    password_bytes = password.encode('utf-8')
    
    if len(password_bytes) > 72:
        # Обрезаем до 72 байт
        password_bytes = password_bytes[:72]
        # Декодируем обратно
        password = password_bytes.decode('utf-8', errors='ignore')
        # Или можно вернуть ошибку:
        # raise ValueError("Password too long. Maximum 72 bytes.")
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет пароль.
    """
    try:
        # Обрезаем пароль для проверки если это bcrypt
        if hashed_password.startswith("$2"):  # bcrypt хэш
            password_bytes = plain_password.encode('utf-8')
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
                plain_password = password_bytes.decode('utf-8', errors='ignore')
        
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False