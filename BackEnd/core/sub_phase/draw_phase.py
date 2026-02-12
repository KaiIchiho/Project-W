from core.sub_phase.phase_base import Phase
from core.sub_phase.clock_phase import ClockPhase

class DrawPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="Draw Phase"
        self.next_phase=ClockPhase
        
    async def on_enter(self, game):
        return super().on_enter(game)
    
    async def on_exit(self, game):
        return super().on_exit(game)
    
    def handle_action(self, game, action,player_id):
        return super().handle_action(game, action,player_id)