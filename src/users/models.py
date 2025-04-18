from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=True)
    # role_id: Mapped[int] = mapped_column(Boolean, nullable=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=0)
    picture: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, onupdate=func.now())