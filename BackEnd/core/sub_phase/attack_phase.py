from core.sub_phase.phase_base import Phase
from core.sub_phase.end_phase import EndPhase
from core.attack_type import AttackType
from core.attack_step.attack_step_base import AttackStep
from core.attack_step.attack_declaration import AttackDeclaration
from core.attack_step.encore import Encore
from core.attack_step.counter import Counter
from core.attack_step.battle import Battle
from core.data_reader import DataReader
from models.playmat import StageStatus
from schemas import event_type,game_flow
from config import setting_ingame
from typing import TYPE_CHECKING,Type
if TYPE_CHECKING:
    from core.game import Game

class AttackPhase(Phase):
    phase_name="Attack Phase"
    next_phase=EndPhase
    
    def __init__(self):
        super().__init__()
        self.handlers[event_type.ATTACK_PHASE_DECLARE]="start_attack"
        self.handlers[event_type.ATTACK_PHASE_STOP_ATTACK]="stop_attakc"
        
        self.step:AttackStep=None
        self.first_step:Type[AttackStep]=AttackDeclaration
        self.encore_step:Type[AttackStep]=Encore
        self.has_attacked_state:dict={}
    
    async def handle_action(self,game:"Game",action:dict,event:str,player_id:int):
        await super().handle_action(game,action,event,player_id)
        await self.handle_step_action(game,action,event,player_id)
    
    async def on_enter(self, game):
        await super().on_enter(game)
        self._is_frozen=True
        self._update_has_attacked_state(game)
        if not self._check_can_attack():
            await self._in_encore_step(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
        
    def _update_has_attacked_state(self,game:"Game"):
        self.has_attacked_state={}
        player_id=game.get_turn_player_id()
        stand_stage=game.get_player_stage_stand_index(player_id)
        rest_stage=game.get_player_stage_rest_index(player_id)
        for stage in stand_stage:
            self.has_attacked_state[stage]=StageStatus.STAND
        for stage in rest_stage:
            self.has_attacked_state[stage]=StageStatus.REST
        
    def _turn_player_char_rest(self,game:"Game",stage_index:int)->bool:
        player_id=game.get_turn_player_id()
        result=game.set_player_stage_status(
            player_id,stage_index,StageStatus.REST)
        if result:
            self.has_attacked_state[stage_index]=StageStatus.REST
        return result
    
    def _check_can_attack(self)->bool:
        for k, v in self.has_attacked_state.items():
            if v == StageStatus.STAND and k in setting_ingame.FRONT_STAGE:
                return True
        return False
    
    async def start_attack(
        self,game:"Game",
        req:game_flow.AttackPhaseDeclareRequest,
        player_id:int
    ):
        if not game.check_is_turn_player_command(player_id):
            return
        if not req.stage_position_index in setting_ingame.FRONT_STAGE:
            return
        if self.step is not None:
            return
        
        state=self.has_attacked_state.get(req.stage_position_index)
        if state is None or state!=StageStatus.STAND:
            return
        if not self._turn_player_char_rest(game,req.stage_position_index):
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
        print("Log: _on_next_attack_step")
        if not self.step:
            return
        await self.step.on_exit(game)
        
        print(f"Log: Current Step Is {self.step.step_name}")
        # アンコールステップの終了
        if isinstance(self.step,self.encore_step):
            print("Log: Current Step Is Encore")
            self._is_frozen=False
            self.is_complete=True
            return
        else:
            print("Log: Current Step Is Not Encore")
        
        if not self.step.next_step:
            self._update_has_attacked_state(game)
            self.step=None
            await self._on_attack_end(game)
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
                    self._update_has_attacked_state(game)
                    self.step=None
                    await self._on_attack_end(game)
                    return
                else:
                    self.step=self.step.next_step.next_step(self._on_next_attack_step,attack_type,stage_position_index)
        else:
            self.step=self.step.next_step(self._on_next_attack_step,attack_type,stage_position_index)
        await self.step.on_enter(game)
        
    async def _in_encore_step(self,game:"Game"):
        self.step=self.encore_step(self._on_next_attack_step)
        if self.step:
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
    
    async def _on_attack_end(self,game:"Game"):
        if not self._check_can_attack():
            await self._in_encore_step(game)
    
    async def stop_attakc(
        self,game:"Game",
        req:game_flow.AttackPhaseStopAttackRequest,
        player_id:int
    ):
        if not game.check_is_turn_player_command(player_id):
            return
        if self.step is not None:
            return
        await self._in_encore_step(game)