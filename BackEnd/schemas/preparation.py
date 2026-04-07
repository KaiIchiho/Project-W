from pydantic import BaseModel
from schemas.common import WSCommonResponseBase
from schemas import event_type

class FirstTurnPlayerData(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.FIRST_TURNPLAYER
    first_turn_player:int=-1
    
