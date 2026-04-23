from core.attack_step.attack_step_base import AttackStep
from core.attack_step.trigger import Trigger
from core.attack_type import AttackType
from core.data_reader import DataReader
from schemas import event_type,game_flow
from config import setting_ingame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class AttackDeclaration(AttackStep):
    step_name="Attack Declaration"
    next_step=Trigger
    def __init__(self,attack_type:AttackType,is_declarated:bool=False):
        super().__init__(attack_type,is_declarated)
        self.handlers[event_type.ATTACK_PHASE_DECLARE]="on_start_attack"
        
    
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)
        
    async def on_start_attack(
        self,game:"Game",
        req:game_flow.AttackPhaseDeclareRequest,
        player_id:int
    ):
        if not game.check_is_turn_player_command(player_id):
            return
        if not req.stage_position_index in setting_ingame.FRONT_STAGE:
            return
        if self.is_declarated:
            return
        
        self.is_declarated=True
        
        player_name=game.get_player_name_by_id(player_id)
        is_first_turn=game.get_current_turn_num()==1
        if not game.player_has_stage_card(player_id,req.stage_position_index):
            success=False
            log=f"{player_name}が選択した舞台はキャラが存在しません"
        else:
            success=True
            log=f"{player_name}は{req.attack_type}の攻撃宣言をしました"
        
        other_index,other_is_empty,other_stage_info=\
            game.get_other_player_stage_info(
                player_id,
                req.stage_position_index,
                ["card_level"])
        other_level=\
            other_stage_info["card_level"]\
                if "card_level" in other_stage_info else -1

        common=DataReader.get_common_data(
            game,success,log,player_id)
        target_stage_position={
            "index":other_index,
            "is_empty":other_is_empty,
            "level":other_level}
        res=game_flow.AttackPhaseDeclareResponse(
            common=common,
            target_stage_position=target_stage_position,
            attack_type=req.attack_type,
            is_first_turn=is_first_turn)
        await game.send_data_to_room(res)