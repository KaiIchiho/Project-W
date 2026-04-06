from pydantic import BaseModel
from schemas.base import WSCommonRequestBase,WSCommonResponseBase
from schemas.common import CommonData

class SelectDeckRequest(WSCommonRequestBase):
    select_deck:int

class StandbyRequest(WSCommonRequestBase):
    pass
class StandbyResponse(WSCommonResponseBase):
    pass

class StartGameResponse(WSCommonResponseBase):
    common:CommonData