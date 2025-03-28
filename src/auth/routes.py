from fastapi import APIRouter

from src.auth.schemas import Register
from src.users.schemas import User
from src.database import database
from src.auth.services import register_user
import src.users.services as user_services
from src.users.exceptions import UserExistException

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=User)
async def register_user_route(user: Register, db: database):
    try:
        if user_services.get_user_by_email(db=db, email=user.email):
            raise UserExistException()
        return register_user(user=user, db=db)
    except Exception as e:
        raise e

