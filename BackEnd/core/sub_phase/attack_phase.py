from core.sub_phase.phase_base import Phase
from core.sub_phase.end_phase import EndPhase
from core.attack_type import AttackType
from core.attack_step.attack_step_base import AttackStep
from core.attack_step.attack_declaration import AttackDeclaration
from core.attack_step.encore import Encore
from core.data_reader import DataReader
from schemas import event_type,game_flow
from config import setting_ingame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class AttackPhase(Phase):
    phase_name="Attack Phase"
    next_phase=EndPhase
    
    def __init__(self):
        super().__init__()
        self.handlers[event_type.ATTACK_PHASE_DECLARE]="on_start_attack"
        
        self.step:AttackStep=None
        self.first_step:AttackStep=AttackDeclaration
        self.encore_step:AttackStep=Encore
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
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
        attack_type=self.parse_attack_type(req.attack_type)
        self._in_first_attack_step(attack_type)
        
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
        print("Log: on_start_attack")
        print(f"Log: other_stage_info: {other_stage_info}")
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
            is_first_turn=is_first_turn
        )
        await game.send_data_to_room(res)
        
    def _in_first_attack_step(self,attack_type:AttackType):
        self.step=self.first_step(attack_type)
    
    def _on_next_attack_step(self):
        if not self.step:
            return
        if not self.step.next_step:
            return
        self.step=self.step.next_step(self.step.attack_type)
        
    async def on_encore(self,game:"Game",action,player_id):
        #if game.attack_step:
        #    return
        #game.attack_step=Encore()
        #game.attack_step.on_enter(game)
        pass
    
    def parse_attack_type(self,type_str:str)->AttackType:
        try:
            return AttackType(type_str)
        except ValueError:
            raise ValueError(f"Attack Type {type_str} Invailed")