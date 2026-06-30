import hashlib
import bcrypt

def hash_password(password: str) -> str:
    """Хэширует пароль с предварительным SHA-256"""
    # 1. Хэшируем пароль через SHA-256 (получаем 32 байта)
    sha256_hash = hashlib.sha256(password.encode('utf-8')).digest()
    
    # 2. Передаём SHA-256 хэш в bcrypt (всегда 32 байта < 72)
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(sha256_hash, salt)
    
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль"""
    # Хэшируем введённый пароль через SHA-256
    sha256_hash = hashlib.sha256(plain_password.encode('utf-8')).digest()
    
    # Сравниваем с bcrypt
    return bcrypt.checkpw(
        sha256_hash,
        hashed_password.encode('utf-8')
    )