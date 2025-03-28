from fastapi import HTTPException


class UserExistException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = {"msg": "User already exists"}
        super().__init__(status_code=self.status_code, detail=self.detail)
