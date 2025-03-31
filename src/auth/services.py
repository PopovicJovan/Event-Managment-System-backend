import random
import string
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from src.auth.exceptions import InvalidCredentialsException
from src.auth.schemas import Register, Login
from src.auth.utils import hash_password, verify_password, get_user_by_google_token, get_user_email_by_google_token
from src.users.models import User
from src.auth.utils import create_access_token, decode_jwt_token
import src.users.services as user_services
from src.users.exceptions import UserExistException
from src.mail.services import send_welcome_email



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

async def google_login(db: Session, token: str):
    try:
        db_user = await get_user_by_google_token(db, token)
        return {
            "user": db_user,
            "token": {
                "token": create_access_token(db_user),
                "type": "access_token"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")


async def google_register(db: Session, token: str):
    email = await get_user_email_by_google_token(token)
    username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # random string , length 8 char
    db_user = User(username=username, email=email)
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

async def google_auth(db: Session, token: str, background_tasks: BackgroundTasks):
    try:
        user = await get_user_by_google_token(db, token)
        if user: return await google_login(db, token)
        return_data = await google_register(db, token)
        if return_data:
            background_tasks.add_task(send_welcome_email, return_data['user'])
        return return_data
    except Exception as e:
        raise e

