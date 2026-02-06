from core.sub_phase.phase_base import Phase
from core.sub_phase.climax_phase import ClimaxPhase

class MainPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="Main Phase"
        self.next_phase=ClimaxPhase
        
    def on_enter(self, game):
        return super().on_enter(game)
    
    def on_exit(self, game):
        return super().on_exit(game)
    
    def handle_action(self, game, action):
        return super().handle_action(game, action)