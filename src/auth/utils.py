from passlib.context import CryptContext
from src.auth.exceptions import InvalidJWTTokenException
from src.users.models import User
from src.config import settings
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user: User):
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    return jwt.encode(data.copy(), key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        raise InvalidJWTTokenException()