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
        await super().on_enter(game)
        await self.draw_initial_hand(game)
    
    def init_playmat(self,game:"Game"):
        result_1,result_2=game.init_players_playmat()
        print("Log: init_playmat")
        print("player 1 Init Playmat: ",result_1)
        print("player 2 Init Playmat: ",result_2)
        
    async def draw_initial_hand(self,game:"Game"):
        print("Log: StandbyPhase draw_initial_hand")
        await game.draw_initial_hand()
        