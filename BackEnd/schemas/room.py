from pydantic import BaseModel
from schemas.object import UserData
from schemas.base import ResponseBase

class CreateRoomRequest(BaseModel):
    # room_id:str
    room_id:int
    room_name:str
    
class CreateRoomResponse(ResponseBase):
    # ok:bool
    # room_id:str
    room_id:int
    room_name:str
    
class EnterRoomRequest(BaseModel):
    # room_id:str
    # user_id:str
    # as_player:bool
    room_id:int
    user:UserData
    
class EnterRoomResponse(ResponseBase):
    # ok:bool
    # room_id:str
    # user_id:str
    room_id:int
    user_id:int
    # log:str
    
class ExitRoomRequest(BaseModel):
    # room_id:str
    user_id:int
    
class ExitRoomResponse(ResponseBase):
    # ok:bool
    # detail:str
    room_id:int
    user_id:int