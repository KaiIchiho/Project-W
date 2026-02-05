from pydantic import BaseModel

class CreateRoomRequest(BaseModel):
    room_id:str
class CreateRoomResponse(BaseModel):
    ok:bool
    room_id:str
class EnterRoomRequest(BaseModel):
    room_id:str
    user_id:str
    as_player:bool
class EnterRoomResponse(BaseModel):
    ok:bool
    room_id:str
    user_id:str
class ExitRoomRequest(BaseModel):
    room_id:str
    user_id:str
class ExitRoomResponse(BaseModel):
    ok:bool
    detail:str
    user_id:str