from functools import wraps
from src.permissions.services import has_permission
from src.users.exceptions import ForbiddenException
from src.database import database
from src.permissions.services import set_permission
from src.users.models import User

def permission_check(permission_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            db = kwargs.get("db")

            if not has_permission(db, permission_name, request):
                raise ForbiddenException()

            return func(*args, **kwargs)

        return wrapper

    return decorator



def set_register_user_permissions(db: database, user: User):
    permissions = ["create_event", "view_events"]
    for name in permissions:
        set_permission(db, user.id, name)