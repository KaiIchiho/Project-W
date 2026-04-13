from core.sub_phase.phase_base import Phase
from core.sub_phase.climax_phase import ClimaxPhase

class MainPhase(Phase):
    phase_name="Main Phase"
    next_phase=ClimaxPhase
    def __init__(self):
        super().__init__()
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    