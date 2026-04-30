from pydantic import BaseModel,Field
from schemas.base import WSRequestBase,WSResponseBase
from schemas.common import WSCommonRequestBase,WSCommonResponseBase
from schemas import event_type,object,sub_request
from typing import Optional

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

class ShuffleResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.SHUFFLE

class NextPhaseRequest(WSCommonRequestBase):
    pass
class NextPhaseResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.NEXT_PHASE

class NextTurnRequest(WSCommonRequestBase):
    pass
class NextTurnResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.NEXT_TURN

class StandPhaseAllStandRepons(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.STAND_PHASE_ALL_STAND

class DrawPhaseDrawSelfResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.DRAW_PHASE_DRAW
    add_hand_card:object.AddCardData
class DrawPhaseDrawOtherResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.DRAW_PHASE_DRAW

class ClockPhaseClockRequest(WSCommonRequestBase):
    # clocked_hand_card:int # index
    clocked_hand_card:sub_request.ClockPhaseClockHandCard
class ClockPhaseClockSelfResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.CLOCK_PHASE_CLOCK
    clocked_hand_card:dict # {card_id}
class ClockPhaseClockOtherResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.CLOCK_PHASE_CLOCK

class ClockPhaseDrowSelfResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.CLOCK_PHASE_DRAW
    add_two_hand_cards:list[dict]=Field(default_factroy=lambda:[{"card_id":-1} for _ in range(2)])
class ClockPhaseDrowOtherResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.CLOCK_PHASE_DRAW

class MainPhaseCharPlayRequest(WSCommonRequestBase):
    chosen_hand_card:int=-1
    stage_position:int=-1
class MainPhaseCharPlayResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.MAIN_PHASE_CHAR_PLAY
    choice_hand_card:str=-1
    stage_position:object.StagePositionData

class MainPhaseEventPlayRequest(WSCommonRequestBase):
    use_card:sub_request.MainPhaseEventPlayUserCard
class MainPhaseEventPlayResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.MAIN_PHASE_EVENT_PLAY

class MainPhaseCharMoveRequest(WSCommonRequestBase):
    stage_position:sub_request.MainPhaseCharMoveStagePos
    target_stage_position:sub_request.MainPhaseCharMoveStagePos
class MainPhaseCharMoveResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.MAIN_PHASE_CHAR_MOVE
    stage_position:dict=Field(default_factroy=dict)
    target_stage_position:dict=Field(default_factroy=dict)

class ClimaxPhaseCXSetRequest(WSCommonRequestBase):
    hand_index:int
class ClimaxPhaseCXSetResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.CLIMAX_PHASE_CX_SET
    cx_is_empty:bool

class AttackPhaseDeclareRequest(WSCommonRequestBase):
    stage_position_index:int
    attack_type:str
class AttackPhaseDeclareResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.ATTACK_PHASE_DECLARE
    target_stage_position:dict=Field(default_factroy=dict)
    attack_type:str
    is_first_turn:bool
    
class AttackPhaseTriggerCheckResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.ATTACK_PHASE_TRIGGER_CHECK
    trigger_card_id:int
    triggers:list[dict]=Field(default_factroy=list)

class AttackPhaseCounterCheckResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.ATTACK_PHASE_COUNTER_CHECK
    is_counter:bool
class AttackPhaseCounterCheckRequest(WSCommonRequestBase):
    chosen_card:Optional[int]
    
class AttackPhaseDamageCheckResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.ATTACK_PHASE_DAMAGE_CHECK
    attack_character:dict=Field(default_factroy=dict)
class AttackPhaseDamageProcessResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.ATTACK_PHASE_DAMAGE_PROCESS
    revealed_card:list[dict]=Field(default_factroy=list)
    is_damage_cancel:bool
class AttackPhaseBattleProcessResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.ATTACK_PHASE_BATTLE_PROCESS
    attack_character:dict=Field(default_factroy=dict)
    defense_character:dict=Field(default_factroy=dict)

class AttackPhaseEncoreRequest(WSCommonRequestBase):
    chosen_cost:str
    order:list[int]=Field(default_factroy=list)
class AttackPhaseEncoreResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.ATTACK_PHASE_ENCORE
    reverse_card_on_stage:list[dict]=Field(default_factroy=list)
    
class AttackPhaseStopAttackRequest(WSCommonRequestBase):
    pass

class EndPhaseCXRemoveResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.END_PHASE_CX_REMOVE
    is_cx_zone_empty:bool

class EndPhaseHandExceedResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.END_PHASE_HAND_EXCEED
    exceed_hand_card_num:int
    
class EndPhaseHandDiscardRequest(WSCommonRequestBase):
    set_waiting_room:list[int]
class EndPhaseHandDiscardResponse(WSCommonResponseBase):
    _DEFAULT_EVENT:str=event_type.END_PHASE_HAND_DISCARD
    throw_hand_card:list[int]

event_req={
    event_type.SWAP_HAND_CARDS:SwapHandCardsRequest,
    event_type.NEXT_PHASE:NextPhaseRequest,
    event_type.NEXT_TURN:NextTurnRequest,
    event_type.CLOCK_PHASE_CLOCK:ClockPhaseClockRequest,
    event_type.MAIN_PHASE_CHAR_PLAY:MainPhaseCharPlayRequest,
    event_type.MAIN_PHASE_EVENT_PLAY:MainPhaseEventPlayRequest,
    event_type.MAIN_PHASE_CHAR_MOVE:MainPhaseCharMoveRequest,
    event_type.CLIMAX_PHASE_CX_SET:ClimaxPhaseCXSetRequest,
    event_type.ATTACK_PHASE_DECLARE:AttackPhaseDeclareRequest,
    event_type.ATTACK_PHASE_COUNTER_CHECK:AttackPhaseCounterCheckRequest,
    event_type.ATTACK_PHASE_ENCORE:AttackPhaseEncoreRequest,
    event_type.ATTACK_PHASE_STOP_ATTACK:AttackPhaseStopAttackRequest,
    event_type.END_PHASE_HAND_DISCARD:EndPhaseHandDiscardRequest
}