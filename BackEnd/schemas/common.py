from pydantic import BaseModel,Field
from schemas.object import PlayerData
from schemas.base import WSResponseBase

class CommonData(WSResponseBase):
    turn_player_user_id:int
    event_user_id: int
    player_1:PlayerData
    player_2:PlayerData
    
class WSCommonResponseBase(BaseModel):
    _DEFAULT_EVENT:str="default_event"
    common:CommonData=Field(
        default_factory=CommonData
    )
    def model_post_init(self, __context=None):
        if self.common.event is None:
            self.common.event = self._DEFAULT_EVENT