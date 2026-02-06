from core.sub_phase.phase_base import Phase
from core.sub_phase.attack_phase import AttackPhase

class ClimaxPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="Climax Phase"
        self.next_phase=AttackPhase
        
    def on_enter(self, game):
        return super().on_enter(game)
    
    def on_exit(self, game):
        return super().on_exit(game)
    
    def handle_action(self, game, action):
        return super().handle_action(game, action)