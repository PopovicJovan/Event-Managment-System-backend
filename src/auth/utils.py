from passlib.context import CryptContext
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from src.auth.exceptions import InvalidJWTTokenException
from src.users.models import User
from src.config import settings
import jwt
from src.auth.config import auth_settings
import src.users.services as user_services


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

def get_user_by_google_token(db: Session, token: str):
    email = get_user_email_by_google_token(token)
    db_user = user_services.get_user_by_email(db=db, email=email)
    if not db_user: return None
    return db_user

def get_user_email_by_google_token(token: str):
    user_info = id_token.verify_oauth2_token(
        token, requests.Request(), auth_settings.GOOGLE_CLIENT_ID
    )
    return user_info.get("email")
