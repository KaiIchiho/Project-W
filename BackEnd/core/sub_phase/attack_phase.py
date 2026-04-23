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
    
    async def handle_action(self,game:"Game",action:dict,event:str,player_id:int):
        # handled = 
        await super().handle_action(game, action, event, player_id)
        # if handled:
        #     return True
        if self.step:
            await self.step.handle_action(game, action, event, player_id)
        # return False
    
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
        other_stage_is_empty=\
            game.get_other_player_stage_is_empty(
                player_id,req.stage_position_index)
        if not AttackType.check_could_attack(attack_type,other_stage_is_empty):
            print("Warning: Could Not Attack")
            return
        await self._in_first_attack_step(game,attack_type)
        
    async def _in_first_attack_step(self,game:"Game",attack_type:AttackType):
        self.step=self.first_step(attack_type)
        await self.step.on_enter(game)
    
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