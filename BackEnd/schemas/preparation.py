from pydantic import BaseModel
from schemas.common import WSCommonResponseBase

class FirstTurnPlayerData(WSCommonResponseBase):
    _DEFAULT_EVENT:str="first_turnplayer"
    first_turn_player:int=-1
    
