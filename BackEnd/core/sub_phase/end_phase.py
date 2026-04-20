from core.sub_phase.phase_base import Phase
from core.data_reader import DataReader
from schemas import event_type,game_flow
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class EndPhase(Phase):
    phase_name="End Phase"
    next_phase=None
    def __init__(self):
        super().__init__()
        
    async def on_enter(self, game):
        await super().on_enter(game)
        await self.remove_turn_player_cx(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    
    async def remove_turn_player_cx(self,game:"Game"):
        has_set_cx=game.remove_cx_card(game.get_turn_player_id())
        player_name=game.get_turn_player_name()
        common=DataReader.get_common_data(
            game,True,
            f"{player_name}のCXカードがCX置き場から控え室に移動しました",
            game.get_turn_player_id())
        res=game_flow.EndPhaseCXRemoveResponse(
            common=common,is_cx_zone_empty=not has_set_cx)
        await game.send_data_to_room(res)