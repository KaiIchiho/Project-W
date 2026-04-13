from core.sub_phase.phase_base import Phase
from core.sub_phase.attack_phase import AttackPhase

class ClimaxPhase(Phase):
    phase_name="Climax Phase"
    next_phase=AttackPhase
    def __init__(self):
        super().__init__()
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    