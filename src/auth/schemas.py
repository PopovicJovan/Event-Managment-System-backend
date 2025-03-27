from pydantic import BaseModel, ConfigDict, EmailStr, model_validator


class UserBase(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)

class Login(UserBase):
    password: str

class Register(Login):
    email: EmailStr
    password_confirmation: str

    @model_validator(mode='before')
    def check_password_confirmation(cls, values):
        password = values.get('password')
        password_confirmation = values.get('password_confirmation')

        if password != password_confirmation:
            raise ValueError('Passwords do not match')

        return values