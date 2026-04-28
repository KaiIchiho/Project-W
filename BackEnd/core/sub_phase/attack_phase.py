from core.sub_phase.phase_base import Phase
from core.sub_phase.end_phase import EndPhase
from core.attack_type import AttackType
from core.attack_step.attack_step_base import AttackStep
from core.attack_step.attack_declaration import AttackDeclaration
from core.attack_step.encore import Encore
from core.attack_step.counter import Counter
from core.attack_step.battle import Battle
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
        await super().handle_action(game,action,event,player_id)
        await self.handle_step_action(game,action,event,player_id)
    
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
        self.step=self.first_step(self._on_next_attack_step,attack_type)
        await self.step.on_enter(game)
    
    async def _on_next_attack_step(self,game:"Game"):
        if not self.step:
            return
        await self.step.on_exit(game)
        if not self.step.next_step:
            self.step=None
            return
        if self.step is self.encore_step:
            self.is_complete=True
            return
        attack_type=self.step.attack_type
        stage_position_index=self.step.stage_position_index
        if self.step.next_step is Counter:
            if AttackType.check_has_counter(attack_type):
                self.step=self.step.next_step(self._on_next_attack_step,attack_type,stage_position_index)
            else:
                self.step=self.step.next_step.next_step(self._on_next_attack_step,attack_type,stage_position_index)
        elif self.step.next_step is Battle:
            if AttackType.check_has_battle(attack_type):
                self.step=self.step.next_step(self._on_next_attack_step,attack_type,stage_position_index)
            else:
                if not self.step.next_step.next_step:
                    self.step=None
                    return
                else:
                    self.step=self.step.next_step.next_step(self._on_next_attack_step,attack_type,stage_position_index)
        else:
            self.step=self.step.next_step(self._on_next_attack_step,attack_type,stage_position_index)
        await self.step.on_enter(game)
        
    async def _in_encore_step(self,game:"Game"):
        await self.step.on_exit(game)
        self.step=self.encore_step()
        await self.step.on_enter(game)
        
    async def handle_step_action(self,game:"Game",action:dict,event:str,player_id:int):
        if not self.step:
            return
        await self.step.handle_action(game, action, event, player_id)
        if self.step.is_complete:
            await self._on_next_attack_step(game)
            
    
    def parse_attack_type(self,type_str:str)->AttackType:
        try:
            return AttackType(type_str)
        except ValueError:
            raise ValueError(f"Attack Type {type_str} Invailed")