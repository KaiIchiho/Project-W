from pydantic import BaseModel
from schemas.base import ResponseBase

class LoginRequest(BaseModel):
    # user_id:int
    user_name:str
    password:str
class LoginResponse(ResponseBase):
    # ok:bool
    user_id:int
    user_name:str
class LogoutRequest(BaseModel):
    user_id:int
class LogoutResponse(ResponseBase):
    # ok:bool
    pass