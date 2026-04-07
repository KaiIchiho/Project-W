from pydantic import BaseModel
from schemas.object import UserData
from schemas.base import ResponseBase,WSRequestBase,WSResponseBase
from schemas import event_type

# class CreateRoomRequest(BaseModel):
#     room_id:int
#     room_name:str
    
# class CreateRoomResponse(ResponseBase):
#     room_id:int
#     room_name:str
    
class EnterRoomRequest(WSRequestBase):
    event:str=event_type.ENTER_ROOM
    room_id:int
    user_is_player:bool
    
class EnterRoomResponse(WSResponseBase):
    event:str=event_type.ENTER_ROOM
    room_id:int
    user_id:int
    user_is_player:bool
    
class ExitRoomRequest(WSRequestBase):
    event:str=event_type.EXIT_ROOM
    user_id:int
    
class ExitRoomResponse(WSResponseBase):
    event:str=event_type.EXIT_ROOM
    room_id:int
    user_id:int