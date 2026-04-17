from core.sub_phase.phase_base import Phase
from core.sub_phase.draw_phase import DrawPhase
from core.data_reader import DataReader
from schemas import event_type,game_flow
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class StandPhase(Phase):
    phase_name="Stand Phase"
    next_phase=DrawPhase
    def __init__(self):
        super().__init__()
    
    async def on_enter(self, game):
        await super().on_enter(game)
        await self.turnplayer_all_stage_stand(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    
    async def turnplayer_all_stage_stand(self,game:"Game"):
        result=game.player_all_stage_rest_stand(game.get_turn_player_id())
        log=""
        player_id=game.get_turn_player_id()
        player_name=game.get_turn_player_name()
        if result:
            log=f"{player_name}の舞台の全てのレスト状態のカードをスタンドさせました"
        common=DataReader.get_common_data(game,result,log,player_id)
        res=game_flow.StandPhaseAllStandRepons(
            common=common)
        await game.send_data_to_room(res)