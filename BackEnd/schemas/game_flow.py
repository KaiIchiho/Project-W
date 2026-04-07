from pydantic import BaseModel
from schemas.base import WSRequestBase,WSResponseBase
from schemas.common import WSCommonResponseBase
from schemas import event_type

class SelectDeckRequest(WSRequestBase):
    select_deck:int=-1

class StandbyRequest(WSRequestBase):
    event:str=event_type.STANDBY
class StandbyResponse(WSResponseBase):
    event:str=event_type.STANDBY

class GameStartResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.GAME_START