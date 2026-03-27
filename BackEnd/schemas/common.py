from pydantic import BaseModel
from schemas.object import PlayerData

class CommonData(BaseModel):
    event:str
    success:bool
    turn_player_user_id:int
    event_user_id: int
    player_1:PlayerData
    player_2:PlayerData