from core.sub_phase.phase_base import Phase
from core.sub_phase.draw_phase import DrawPhase

class StandPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="Stand Phase"
        self.next_phase=DrawPhase
    
    def on_enter(self, game):
        #return super().on_enter(game)
        game.send_message(None,"Enter Start Phase",None)
    
    def on_exit(self, game):
        return super().on_exit(game)
    
    def handle_action(self, game, action,player_id:str):
        return super().handle_action(game, action,player_id)