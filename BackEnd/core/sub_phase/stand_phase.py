from core.sub_phase.phase_base import Phase
from core.sub_phase.draw_phase import DrawPhase

class StandPhase(Phase):
    phase_name="Stand Phase"
    next_phase=DrawPhase
    def __init__(self):
        super().__init__()
    
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    