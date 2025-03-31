from fastapi import Header

from src.auth.services import get_user_by_token
from src.users.exceptions import ForbiddenException
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()  # Logovanje u konzolu
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def is_user_admin(authorization: str = Header(...)):
    token = authorization.split()[1]
    try:
        user_data = get_user_by_token(token)
        logger.info(user_data)
        if not user_data['admin']: raise ForbiddenException()
        return True
    except Exception as e:
        raise ForbiddenException()
