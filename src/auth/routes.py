from fastapi import APIRouter, Header
from src.auth.exceptions import InvalidJWTTokenException
from src.auth.schemas import Register, AuthReturnSchema, Login
from src.database import database
from src.auth.services import register_user, login_user, get_user_by_token
from src.users.schemas import User as UserSchema
from src.users.services import get_user_by_id

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])



@router.post("/register", response_model=AuthReturnSchema)
async def register_user_route(user: Register, db: database):
    try:
        return register_user(user=user, db=db)
    except Exception as e:
        raise e

@router.post("/login", response_model=AuthReturnSchema)
async def login_user_route(user: Login, db: database):
    try:
        return login_user(db=db, login_data=user)
    except Exception as e:
        raise e


@router.get("/me", response_model=UserSchema)
async def get_user( db: database, authorization: str = Header(...)):
    try:
        token = authorization.split()[1]
        payload = get_user_by_token(token)
        return get_user_by_id(db, payload.get("id"))
    except InvalidJWTTokenException as e:
        raise e
    except Exception as e:
        raise e
