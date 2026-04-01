from pydantic import BaseModel
from schemas.base import ResponseBase

class DeckInfo(BaseModel):
    deck_id:int
    deck_name:str
class DeckListRequest(BaseModel):
    pass
class DeckListResponse(BaseModel):
    deck_list:list[DeckInfo]

class SelectDeckResquest(BaseModel):
    select_deck:int
class SelectDeckResponse(ResponseBase):
    pass

#class CardInfoResponse(BaseModel):
