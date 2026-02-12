from core.sub_phase.phase_base import Phase
from core.sub_phase.clock_phase import ClockPhase

class DrawPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="Draw Phase"
        self.next_phase=ClockPhase
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    
    async def handle_action(self, game, action,player_id):
        await super().handle_action(game, action,player_id)