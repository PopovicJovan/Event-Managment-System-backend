from pydantic import BaseModel, ConfigDict
from  datetime import datetime

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    id: int
    username: str
    email: str
    admin: bool
    created_at: datetime
