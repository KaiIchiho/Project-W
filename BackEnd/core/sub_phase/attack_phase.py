from core.sub_phase.phase_base import Phase
from core.sub_phase.end_phase import EndPhase
from core.attack_type import AttackType
from core.attack_step.attack_step_base import AttackStep
from core.attack_step.attack_declaration import AttackDeclaration
from core.attack_step.encore import Encore
from core.data_reader import DataReader
from schemas import event_type,game_flow
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class AttackPhase(Phase):
    phase_name="Attack Phase"
    next_phase=EndPhase
    def __init__(self):
        super().__init__()
        self.handlers[event_type.ATTACK_PHASE_DECLARE]="on_start_attack"
        # self.handlers[]="on_encore"
        
        self.step:AttackStep=None
        self.first_step:AttackStep=AttackDeclaration
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
        
    async def on_start_attack(self,game:"Game",action,player_id):
        #if game.attack_step:
        #    return
        #game.attack_step=AttackDeclaration()
        #game.attack_step.on_enter(game)
        pass
        
    async def on_encore(self,game:"Game",action,player_id):
        #if game.attack_step:
        #    return
        #game.attack_step=Encore()
        #game.attack_step.on_enter(game)
        pass