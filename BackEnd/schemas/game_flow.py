from pydantic import BaseModel
from schemas.base import WSRequestBase,WSResponseBase
from schemas.common import CommonData

class SelectDeckRequest(WSRequestBase):
    select_deck:int

class StandbyRequest(WSRequestBase):
    pass
class StandbyResponse(WSResponseBase):
    pass

class StartGameResponse(BaseModel):
    common:CommonData