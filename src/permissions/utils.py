from functools import wraps
from src.permissions.services import has_permission
from src.users.exceptions import ForbiddenException


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