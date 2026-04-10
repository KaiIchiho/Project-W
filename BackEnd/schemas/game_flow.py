from pydantic import BaseModel
from schemas.base import WSRequestBase,WSResponseBase
from schemas.common import WSCommonRequestBase,WSCommonResponseBase
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

class FirstTurnPlayerResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.FIRST_TURNPLAYER
    first_turn_player:int=-1
    
class GameStartResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.GAME_START

class DrawInitialHandResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.DRAW_INITIAL_HAND

class SwapHandCardsRequest(WSCommonRequestBase):
    hand_index:list[int]
    
class SwapHandCardsResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.SWAP_HAND_CARDS

class OnPhaseChangedResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.ON_PHASE_CHANGED

event_req={
    event_type.SWAP_HAND_CARDS:SwapHandCardsRequest
}