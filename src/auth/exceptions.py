from fastapi import HTTPException



class InvalidCredentialsException(HTTPException):
    def __init__(self):
        self.status_code = 401
        self.detail = {"msg": "Invalid credentials"}
        super().__init__(status_code=self.status_code, detail=self.detail)

class InvalidJWTTokenException(HTTPException):
    def __init__(self):
        self.status_code = 401
        self.detail = {"msg": "Invalid token"}
        super().__init__(status_code=self.status_code, detail=self.detail)