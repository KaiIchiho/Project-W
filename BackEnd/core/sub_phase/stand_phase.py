from core.sub_phase.phase_base import Phase
from core.sub_phase.draw_phase import DrawPhase

class StandPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="Stand Phase"
        self.next_phase=DrawPhase
    
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    
    async def handle_action(self, game, action,player_id:str):
        await super().handle_action(game, action,player_id)