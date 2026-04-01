from pydantic import BaseModel
from schemas.object import PlayerData
from schemas.base import WSCommonResponseBase

class CommonData(WSCommonResponseBase):
    turn_player_user_id:int
    event_user_id: int
    player_1:PlayerData
    player_2:PlayerData