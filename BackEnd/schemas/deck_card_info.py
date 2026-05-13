from pydantic import BaseModel
from schemas import event_type
from schemas.base import WSRequestBase,WSResponseBase

class DeckInfo(BaseModel):
    deck_id:int
    deck_name:str
class DeckListRequest(BaseModel):
    pass
class DeckListResponse(BaseModel):
    deck_list:list[DeckInfo]

class CardInfoRequest(WSRequestBase):
    event:str=event_type.CARD_INFO
    card_id:int
    columns:list[str]
    
class CardInfoResponse(WSResponseBase):
    event:str=event_type.CARD_INFO
    card_id:int
    columns:dict
    
