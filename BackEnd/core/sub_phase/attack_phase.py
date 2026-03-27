from core.sub_phase.phase_base import Phase
from core.sub_phase.end_phase import EndPhase
#from core.attack_step.attack_declaration import AttackDeclaration
#from core.attack_step.encore import Encore
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class AttackPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="Attack Phase"
        self.next_phase=EndPhase
        self.handlers["start_attack"]="on_start_attack"
        self.handlers["encore"]="on_encore"
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    
    async def handle_action(self, game, action,player_id):
        await super().handle_action(game, action,player_id)
        
        if not game.attack_step:
            return
        if game.attack_step.is_complete==True:
            game.attack_step.on_next_step()
        
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