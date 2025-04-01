from fastapi import APIRouter, Header
import src.users.services as user_services
from src.database import database
from src.permissions.utils import permission_check
from typing import List
from src.users.schemas import User as UserSchema
from src.users.services import get_user_by_id
from src.auth.services import get_user_by_token
from src.auth.exceptions import InvalidJWTTokenException
from fastapi import Request


router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/", response_model=List[UserSchema])
@permission_check(permission_name="view_users")
def get_users(db: database, request: Request):
    return user_services.get_all_users(db)

@router.get("/me", response_model=UserSchema)
def get_user(db: database, authorization: str = Header(...)):
    try:
        token = authorization.split()[1]
        payload = get_user_by_token(token)
        return get_user_by_id(db, payload.get("id"))
    except InvalidJWTTokenException as e:
        raise e
    except Exception as e:
        raise e

@router.get("/{user_id}", response_model=UserSchema)
@permission_check(permission_name="view_user")
def get_user(user_id: int, db: database, request: Request):
    return user_services.get_user_by_id(db, user_id)

