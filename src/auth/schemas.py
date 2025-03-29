from pydantic import BaseModel, ConfigDict, EmailStr, model_validator, field_validator, Field
from src.users.schemas import User as UserSchema

class UserBase(BaseModel):
    email: str = Field(..., alias="email")

    model_config = ConfigDict(from_attributes=True)

class Login(UserBase):
    password: str = Field(..., min_length=8, alias="password")

class Token(BaseModel):
    token: str = Field(...)
    type: str = "access_token"


class Register(Login):
    username: str = Field(..., min_length=5, alias="username")
    password_confirmation: str = Field(..., min_length=8, alias="password_confirmation")


    @field_validator("password_confirmation")
    @classmethod
    def validate_password_confirmation(cls, value, values):
        if "password" in values.data and value != values.data["password"]:
            raise ValueError("Passwords do not match")
        return value

    @field_validator("email")
    @classmethod
    def validate_password_confirmation(cls, value):
        if not '@' in value:
            raise ValueError("Email adress is not valid")
        return value

class AuthReturnSchema(BaseModel):
    user: UserSchema
    token: Token