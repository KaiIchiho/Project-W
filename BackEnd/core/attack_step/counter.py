from core.attack_step.attack_step_base import AttackStep
from core.attack_step.damage import Damage
from core.attack_type import AttackType
from core.data_reader import DataReader
from schemas import event_type,game_flow
from typing import TYPE_CHECKING,Callable,Awaitable
if TYPE_CHECKING:
    from core.game import Game

class Counter(AttackStep):
    step_name="Counter"
    next_step=Damage
    is_waiting_request=False
    def __init__(self,auto_next_step:Callable[["Game"],Awaitable[None]],attack_type:AttackType,stage_position_index:int):
        super().__init__(auto_next_step,attack_type,True,stage_position_index)
        self.handlers[event_type.ATTACK_PHASE_COUNTER_CHECK]="other_player_check_counter"
        
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
        await self.counter_check_response(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)
        
    async def counter_check_response(self,game:"Game"):
        player_id=game.get_other_player_id()
        
        # common_self=DataReader.get_common_data(
        #     game,True,"",player_id)
        # res_self=game_flow.AttackPhaseCounterCheckResponse(
        #     common=common_self,
        #     is_counter=False)# Temporary
        
        common_other=DataReader.get_common_data(
            game,True,"カウンターを行いますか",player_id)
        res_other=game_flow.AttackPhaseCounterCheckResponse(
            common=common_other,
            is_counter=False)# Temporary
        
        self.set_waiting_event(common_other.event,player_id)
        await game.send_data_to_player(player_id,res_other)
        self.is_waiting_request=True
    
    async def other_player_check_counter(
        self,game:"Game",
        req:game_flow.AttackPhaseCounterCheckRequest,
        player_id:int
    ):
        if player_id!=game.get_other_player_id():
            return
        if not self.is_waiting_request:
            return
        
        if req.chosen_card is not None:
            pass
        
        self.is_waiting_request=False
        self.is_complete=True