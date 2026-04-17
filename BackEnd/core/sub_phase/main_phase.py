from core.sub_phase.phase_base import Phase
from core.sub_phase.climax_phase import ClimaxPhase
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
        self.handlers[event_type.MAIN_PHASE_EVENT_PLAY]="event_play"
        self.handlers[event_type.MAIN_PHASE_CHAR_MOVE]="char_move"
        
    async def on_enter(self, game:"Game"):
        await super().on_enter(game)
    
    async def on_exit(self, game:"Game"):
        await super().on_exit(game)
    
    async def char_play(
        self,game:"Game",
        req:game_flow.MainPhaseCharPlayRequest,
        player_id:int
    ):
        if not game.check_is_turn_player_command(player_id):
            return
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
    
    async def event_play(
        self,game:"Game",
        req:game_flow.MainPhaseEventPlayRequest,
        player_id:int
    ):
        if not game.check_is_turn_player_command(player_id):
            return
        hand_index=req.use_card.hand_index
        success=False
        log=""
        # if hand_index is not None:
        success=game.play_event_card(
            player_id,hand_index)
        
        player_name=game.get_player_name_by_id(player_id)
        if success:
            log=f"{player_name}はイベントカードをプレイしました"
        else:
            log=f"{player_name}はイベントカードをプレイできませんでした"
        
        common=DataReader.get_common_data(
            game,success,log,player_id)
        res=game_flow.MainPhaseEventPlayResponse(
            common=common)
        await game.send_data_to_room(res)
        
        # Temporary
        game.check_command_player(player_id).process_resolution()
        
    async def char_move(
        self,game:"Game",
        req:game_flow.MainPhaseCharMoveRequest,
        player_id:int
    ):
        if not game.check_is_turn_player_command(player_id):
            return
        result,ori_card_id,tar_card_id,ori_origin_status,tar_origin_status,ori_card_status,tar_card_status\
        =game.move_stage_char(player_id,req.stage_position.index,req.target_stage_position.index)
        stage_position={
            "index":req.stage_position.index,
            "card_id":tar_card_id,
            "origin_status":ori_origin_status,
            "card_status": ori_card_status,
        }
        target_stage_position={
            "index":req.target_stage_position.index,
            "card_id":ori_card_id,
            "origin_status":tar_origin_status,
            "card_status":tar_card_status,
        }
        log=""
        player_name=game.get_player_name_by_id(player_id)
        if result:
            log=f"{player_name}はキャラクターカードの枠を移動しました"
        else:
            log=f"{player_name}はキャラクターカードの枠を移動できませんでした"
        common=DataReader.get_common_data(
            game,result,log,player_id)
        res=game_flow.MainPhaseCharMoveResponse(
            common=common,
            stage_position=stage_position,
            target_stage_position=target_stage_position)
        await game.send_data_to_room(res)
        