from core.sub_phase.phase_base import Phase
from core.sub_phase.attack_phase import AttackPhase
from core.data_reader import DataReader
from schemas import event_type,game_flow
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class ClimaxPhase(Phase):
    phase_name="Climax Phase"
    next_phase=AttackPhase
    def __init__(self):
        super().__init__()
        self.handlers[event_type.CLIMAX_PHASE_CX_SET]="player_set_cx"
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    
    async def player_set_cx(
        self,game:"Game",
        req:game_flow.ClimaxPhaseCXSetRequest,
        player_id:int
    ):
        if not game.check_is_turn_player_command(player_id):
            return
        success,has_set_cx=game.set_cx_card(player_id,req.hand_index)
        log=""
        player_name=game.get_player_name_by_id(player_id)
        if success:
            log=f"{player_name}は手札からCXカードをCX置き場に置くことが成功しました"
        else:
            log=f"{player_name}は手札からCXカードをCX置き場に置くことが失敗しました"
        
        common=DataReader.get_common_data(game,success,log,player_id)
        res=game_flow.ClimaxPhaseCXSetResponse(
            common=common,cx_is_empty=not has_set_cx)
        await game.send_data_to_room(res)