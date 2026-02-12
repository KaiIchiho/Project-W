from core.sub_phase.phase_base import Phase
from core.sub_phase.draw_phase import DrawPhase

class StandPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="Stand Phase"
        self.next_phase=DrawPhase
    
    async def on_enter(self, game):
        return super().on_enter(game)
    
    async def on_exit(self, game):
        return super().on_exit(game)
    
    def handle_action(self, game, action,player_id:str):
        return super().handle_action(game, action,player_id)