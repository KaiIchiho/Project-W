from core.sub_phase.phase_base import Phase
from core.sub_phase.main_phase import MainPhase

class ClockPhase(Phase):
    phase_name="Clock Phase"
    next_phase=MainPhase
    def __init__(self):
        super().__init__()
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    