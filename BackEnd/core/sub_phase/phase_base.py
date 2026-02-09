#from enum import Enum,auto

#class Phase(Enum):
#    STAND=auto()
#    DRAW=auto()
#    CLOCK=auto()
#    MAIN=auto()
#    CLIMAX=auto()
#    ATTACK=auto()
#    END=auto()

from services.sub_command.next_turn_command import NextTurnCommand
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class Phase:
    handlers={
        "next_phase":"on_next_phase",
        "next_turn":"on_next_turn"
        }
    is_complete=False
    phase_name="phase_base"
    next_phase=None
    
    def on_enter(self,game:"Game"):
        pass
    def on_exit(self,game:"Game"):
        pass
    def handle_action(self,game:"Game",action:dict)->str:
        handler_name=self.handlers.get(action.get("type"))
        if not handler_name:
            raise ValueError("Action Not Found")
        handler=getattr(self,handler_name)
        return handler(game,action)
    
    def on_next_phase(self,game:"Game",action:dict):
        if self.next_phase is None:
            return self.on_next_turn(game,action)
        else:
            game.phase=self.next_phase()
            return f"Next Phase : {game.phase.phase_name}"
            
    def on_next_turn(self,game:"Game",action:dict):
        next_player=game.start_next_turn()
        return f"Next Is Player {next_player}'s Turn"