from sqlalchemy.orm import Session
from src.auth.exceptions import InvalidCredentialsException
from src.auth.schemas import Register, Login
from src.auth.utils import hash_password, verify_password
from src.users.models import User
from src.auth.utils import create_access_token, decode_jwt_token
import src.users.services as user_services
from src.users.exceptions import UserExistException


def register_user(db: Session, user: Register) -> dict:
    if user_services.get_user_by_email(db=db, email=user.email):
        raise UserExistException()
    hashed_password = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=str(user.email),
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


    return {
        "user": db_user,
        "token": {
            "token": create_access_token(db_user),
            "type": "access_token"
        }
    }


def login_user(db: Session, login_data: Login) -> dict:
    db_user = user_services.get_user_by_email(db=db, email=login_data.email)

    if not db_user: raise InvalidCredentialsException()
    if not verify_password(login_data.password, str(db_user.password)): raise InvalidCredentialsException()

    return {
        "user": db_user,
        "token": {
            "token": create_access_token(db_user),
            "type": "access_token"
        }
    }


def get_user_by_token(token: str) -> dict:
    return decode_jwt_token(token)

