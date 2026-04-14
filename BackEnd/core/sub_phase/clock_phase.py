from core.sub_phase.phase_base import Phase
from core.sub_phase.main_phase import MainPhase
from schemas import event_type,game_flow
from core.data_reader import DataReader
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class ClockPhase(Phase):
    phase_name="Clock Phase"
    next_phase=MainPhase
    def __init__(self):
        super().__init__()
        self.handlers[event_type.CLOCK_PHASE_CLOCK]="start_clock"
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    
    async def start_clock(self,game:"Game",req:game_flow.ClockPhaseClockRequest,player_id:int):
        card_id=game._set_hand_to_clock(player_id,req.clocked_hand_card)
        result=False
        log=""
        if card_id!=-1:
            result=True
            log=f"{card_id}をクロック置き場に置きました"
        else:
            log=f"{card_id}をクロック置き場に置きませんでした"
        
        other_player_id=game.get_other_player_id()
        common=DataReader.get_common_data(game,result,log,player_id)
        res_self=game_flow.ClockPhaseClockSelfResponse(
            common=common,
            clocked_hand_card=card_id)
        res_other=game_flow.ClockPhaseClockOtherResponse(
            common=common)
        await game.send_data_to_room_except_target(other_player_id,res_self)
        await game.send_data_to_player(other_player_id,res_other)