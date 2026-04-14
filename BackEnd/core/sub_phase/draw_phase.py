from core.sub_phase.phase_base import Phase
from core.sub_phase.clock_phase import ClockPhase
from schemas import event_type,game_flow
from core.data_reader import DataReader
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class DrawPhase(Phase):
    phase_name="Draw Phase"
    next_phase=ClockPhase
    def __init__(self):
        super().__init__()
        
    async def on_enter(self, game):
        await super().on_enter(game)
        await self.draw_drap_phase_hand(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    
    async def draw_drap_phase_hand(self,game:"Game"):
        success=False
        log=""
        player_id=-1
        player=game.turn_player
        if player:
            player_id=player.player_id
            card_id=player.draw()
            add_card_data=DataReader.get_add_card_data(card_id)
            success=True
            log=f"{player.name}はドローしました"
        else:
            log=f"{player.name}はドローできませんでした"
        
        other_player_id=game.get_other_player_id()
        common=DataReader.get_common_data(
            game,success,log,player_id
        )
        res_self=game_flow.DrawPhaseDrawSelfResponse(
            common=common,add_hand_card=add_card_data)
        res_other=game_flow.DrawPhaseDrawOtherResponse(
            common=common)
        await game.send_data_to_room_except_target(other_player_id,res_self)
        await game.send_data_to_player(other_player_id,res_other)