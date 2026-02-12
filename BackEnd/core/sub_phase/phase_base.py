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
    def handle_action(self,game:"Game",action:dict,player_id:str)->dict:
        handler_name=self.handlers.get(action.get("type"))
        if not handler_name:
            raise ValueError("Action Not Found")
        handler=getattr(self,handler_name)
        
        text=""
        identity=game.check_player_identity_by_id(player_id)
        if identity!=-1:
            text=f"Player {identity}'s Action: "
        
        message=handler(game,action,player_id)
        if message.get("room") is not None:
            print(f"message: {message}")
            message["room"]=text+message["room"]
        
        return message
    
    def on_next_phase(self,game:"Game",action:dict,player_id:str):
        if not game.check_is_action_player_command(player_id):
            return game.create_message("Not Your Turn",None)
        if self.next_phase is None:
            print("Log: on_next_phase, Next Phase Is None")
            return self.on_next_turn(game,action,player_id)
        else:
            print("Log: on_next_phase, Next Phase Is Not None")
            game.phase=self.next_phase()
            return game.create_message(None,f"Next Phase : {game.phase.phase_name}")
            
    def on_next_turn(self,game:"Game",action:dict,player_id:str):
        if not game.check_is_action_player_command(player_id):
            return game.create_message("Not Your Turn",None)
        next_player=game.start_next_turn()
        return game.create_message(None,f"Next Is Player {next_player}'s Turn")