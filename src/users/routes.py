from fastapi import APIRouter
from fastapi.params import Depends
import src.users.services as user_services
from src.database import database
from src.users.utils import is_user_admin
from typing import List
from src.users.schemas import User as UserSchema


router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/", response_model=List[UserSchema], dependencies=[Depends(is_user_admin)])
def get_users(db: database):
    return user_services.get_all_users(db)

@router.get("/{user_id}", response_model=UserSchema, dependencies=[Depends(is_user_admin)])
def get_user(user_id: int, db: database):
    return user_services.get_user_by_id(db, user_id)

