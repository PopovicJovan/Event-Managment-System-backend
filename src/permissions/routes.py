from fastapi import APIRouter, Request
from src.database import database
from src.permissions.services import get_all_permission, set_permission, has_permission, delete_permission
from src.permissions.utils import permission_check

router = APIRouter(prefix="/api/v1/permissions", tags=["permissions"])

@router.get("/")
def get_permissions(db: database):
    try:
        return get_all_permission(db)
    except Exception as e:
        raise e

@router.post("/{user_id}/assign/{permission_id}")
@permission_check(permission_name="set_permissions")
def assign_permission(db: database, user_id: int, permission_id: int, request: Request):
    try:
        set_permission(db, user_id, permission_id)
    except Exception as e:
        raise e


@router.post("/{user_id}/assign/{permission_id}")
@permission_check(permission_name="remove_permissions")
def remove_permission(db: database, user_id: int, permission_id: int, request: Request):
    try:
        delete_permission(db, user_id, permission_id)
    except Exception as e:
        raise e




