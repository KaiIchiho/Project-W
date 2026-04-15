from core.sub_phase.phase_base import Phase
from core.sub_phase.climax_phase import ClimaxPhase
from services.parse_model import parse_model
from core.data_reader import DataReader
from schemas import event_type,game_flow
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class MainPhase(Phase):
    phase_name="Main Phase"
    next_phase=ClimaxPhase
    def __init__(self):
        super().__init__()
        self.handlers[event_type.MAIN_PHASE_CHAR_PLAY]="char_play"
        
    async def on_enter(self, game:"Game"):
        await super().on_enter(game)
    
    async def on_exit(self, game:"Game"):
        await super().on_exit(game)
    
    async def char_play(
        self,game:"Game",
        req:game_flow.MainPhaseCharPlayRequest,
        player_id:int
    ):
        has_card,success=game.play_char_card(
            player_id,
            req.chosen_hand_card,
            req.stage_position)
        log=""
        player_name=game.get_player_name_by_id(player_id)
        if success:
            log=f"{player_name}は手札をステージに置きました"
            if has_card:
                log+="、ステージの元のカードが控え室へ移動しました"
        else:
            log=f"{player_name}は手札をステージに置けませんでした"
        
        stage_position=DataReader.get_stage_position_data_pack(
            req.stage_position,has_card)
        common=DataReader.get_common_data(
            game,success,log,player_id)
        res=game_flow.MainPhaseCharPlayResponse(
            common=common,
            stage_position=stage_position)
        await game.send_data_to_room(res)
        