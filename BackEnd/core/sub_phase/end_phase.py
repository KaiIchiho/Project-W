from core.sub_phase.phase_base import Phase

class EndPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="End Phase"
        self.next_phase=None
        
    def on_enter(self, game):
        return super().on_enter(game)
    
    def on_exit(self, game):
        return super().on_exit(game)
    
    def handle_action(self, game, action):
        return super().handle_action(game, action)