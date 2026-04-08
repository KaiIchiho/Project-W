from core.sub_phase.phase_base import Phase
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class StandbyPhase(Phase):
    def __init__(self):
        super().__init__()
        self.phase_name="Standby Phase"
        self.next_phase=None
        self.handlers={
            "draw_initial_hand":"draw_initial_hand"
        }
        
    async def on_enter(self,game:"Game"):
        super().on_enter(game)
        self.draw_initial_hand(game)
        
    def draw_initial_hand(self,game:"Game"):
        print("StandbyPhase draw_initial_hand")
        