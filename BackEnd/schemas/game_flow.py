from pydantic import BaseModel
from schemas.base import WSCommonRequestBase,WSCommonResponseBase

class SelectDeckRequest(WSCommonRequestBase):
    select_deck:int

class StandbyRequest(WSCommonRequestBase):
    pass
class StandbyResponse(WSCommonResponseBase):
    pass
