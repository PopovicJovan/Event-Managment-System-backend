from fastapi import Header, Request
from soupsieve.util import lower
from sqlalchemy.orm import Session
import src.users.services as user_service
from src.permissions.exceptions import PermissionNotExistException
from src.users.models import User
from src.auth.utils import decode_jwt_token
from src.auth.exceptions import InvalidJWTTokenException


from src.permissions.models import Permission
from src.users.exceptions import UserNotExistException, ForbiddenException


def get_permission_by_name(db: Session, name: str):
    return db.query(Permission).filter(Permission.name == lower(name)).first()

def get_permission_by_id(db: Session, permission_id: int):
    return db.query(Permission).filter(Permission.id == permission_id).first()

def set_permission(db: Session, user_id: int, permission_name: str):
    user = user_service.get_user_by_id(db, user_id)
    permission = get_permission_by_name(db, permission_name)
    if not user: raise UserNotExistException()
    if not permission: raise PermissionNotExistException()

    if not permission in user.permissions:
        user.permissions.append(permission)
        db.commit()

    return None

def delete_permission(db: Session, user_id: int, permission_id: int):
    user = user_service.get_user_by_id(db, user_id)
    permission = get_permission_by_id(db, permission_id)
    if not user: raise UserNotExistException()
    if not permission: raise PermissionNotExistException()

    if permission in user.permissions:
        user.permissions.remove(permission)
        db.commit()

    return None


def get_all_permission(db: Session):
    return db.query(Permission).all()

def has_permission(db: Session, permission_name: str, request: Request):
    token = request.headers.get("Authorization")
    if not token: raise InvalidJWTTokenException()

    token = token.split()[1]

    user = user_service.get_user_by_id(db, decode_jwt_token(token)['id'])
    return len([p for p in user.permissions if p.name == permission_name]) > 0








