from pydantic import BaseModel
from schemas.base import ResponseBase,WSRequestBase,WSResponseBase
from schemas.common import WSCommonResponseBase
from schemas import event_type

class SelectDeckRequest(WSRequestBase):
    event:str=event_type.SELECT_DECK
    select_deck:int=-1
class SelectDeckResponse(WSResponseBase):
    event:str=event_type.SELECT_DECK
    pass

class StandbyRequest(WSRequestBase):
    event:str=event_type.STANDBY
class StandbyResponse(WSResponseBase):
    event:str=event_type.STANDBY

class GameStartResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.GAME_START