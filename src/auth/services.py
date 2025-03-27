from sqlalchemy.orm import Session
from src.auth.schemas import Register
from src.auth.utils import hash_password
from src.users.models import User


def register_user(db: Session, user: Register):
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=str(user.email),
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user