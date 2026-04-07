from pydantic import BaseModel
from schemas.object import UserData
from schemas.base import ResponseBase,WSRequestBase,WSResponseBase

# class CreateRoomRequest(BaseModel):
#     room_id:int
#     room_name:str
    
# class CreateRoomResponse(ResponseBase):
#     room_id:int
#     room_name:str
    
class EnterRoomRequest(WSRequestBase):
    room_id:int
    user_is_player:bool
    
class EnterRoomResponse(WSResponseBase):
    room_id:int
    user_id:int
    user_is_player:bool
    
class ExitRoomRequest(WSRequestBase):
    user_id:int
    
class ExitRoomResponse(WSResponseBase):
    room_id:int
    user_id:int