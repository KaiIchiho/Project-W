from pydantic import BaseModel
from schemas.object import UserData
from schemas.base import ResponseBase,WSCommonRequestBase,WSCommonResponseBase

# class CreateRoomRequest(BaseModel):
#     room_id:int
#     room_name:str
    
# class CreateRoomResponse(ResponseBase):
#     room_id:int
#     room_name:str
    
class EnterRoomRequest(WSCommonRequestBase):
    room_id:int
    user_is_player:bool
    
class EnterRoomResponse(WSCommonResponseBase):
    room_id:int
    user_id:int
    user_is_player:bool
    
class ExitRoomRequest(WSCommonRequestBase):
    user_id:int
    
class ExitRoomResponse(WSCommonResponseBase):
    room_id:int
    user_id:int