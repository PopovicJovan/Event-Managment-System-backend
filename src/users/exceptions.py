from fastapi import HTTPException


class UserExistException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = {"msg": "User already exists"}
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserNotExistException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = {"msg": "User does not exist"}
        super().__init__(status_code=self.status_code, detail=self.detail)

class ForbiddenException(HTTPException):
    def __init__(self):
        self.status_code = 403
        self.detail = {"msg": "You do not have permission to access this resource"}
        super().__init__(status_code=self.status_code, detail=self.detail)