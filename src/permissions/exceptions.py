from fastapi import HTTPException


class PermissionExistException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = {"msg": "Permission already exists"}
        super().__init__(status_code=self.status_code, detail=self.detail)

class PermissionNotExistException(HTTPException):
    def __init__(self):
        self.status_code = 400
        self.detail = {"msg": "Permission does not exist"}
        super().__init__(status_code=self.status_code, detail=self.detail)