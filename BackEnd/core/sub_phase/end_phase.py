from core.sub_phase.phase_base import Phase

class EndPhase(Phase):
    phase_name="End Phase"
    next_phase=None
    def __init__(self):
        super().__init__()
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    