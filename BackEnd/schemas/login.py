from pydantic import BaseModel

class LoginRequest(BaseModel):
    user_id:str
    user_name:str
class LoginResponse(BaseModel):
    ok:bool
    user_id:str
    user_name:str
class LogoutRequest(BaseModel):
    user_id:str
class LogoutResponse(BaseModel):
    ok:bool