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
    
    async def on_enter(self,game:"Game"):
        await game.send_message(None,f"Enter {self.phase_name}",game.turn_player.player_id)
    async def on_exit(self,game:"Game"):
        await game.send_message(None,f"Exit {self.phase_name}",game.turn_player.player_id)
    
    async def send_message_list(self,game:"Game",message_list:list[dict],default_player_id:str):
        for message in message_list:
            room_message_text=""
            player_id=message.get("player_id")
            if player_id is None:
                player_id=default_player_id
            identity=game.check_player_identity_by_id(player_id)
            if identity!=-1:
                room_message_text=f"Player {identity}'s Action: "
                
            if message.get("room") is not None:
                message["room"]=room_message_text+message["room"]
            await game.send_message_backage(message,player_id)

    async def handle_action(self,game:"Game",action:dict,player_id:str)->dict:
        handler_name=self.handlers.get(action.get("type"))
        if not handler_name:
            raise ValueError("Action Not Found")
        handler=getattr(self,handler_name)
        
        messages=await handler(game,action,player_id)
        
        await self.send_message_list(game,messages,player_id)
    
    async def on_next_phase(self,game:"Game",action:dict,player_id:str):
        messages=[]
        if not game.check_is_turn_player_command(player_id):
            message=game.create_message("Not Your Turn",None)
            messages.append(message)
            return messages
        
        print(f"Log: on_next_phase, Now Phase Is {self.phase_name}")
        game.phase.on_exit(game)
        if self.next_phase is None:
            print("Log: on_next_phase, Next Phase Is None")
            messages=await self.on_next_turn(game,action,player_id)
        else:
            print("Log: on_next_phase, Next Phase Is Not None")
            game.phase=self.next_phase()
            message=game.create_message(None,f"Next Phase : {game.phase.phase_name}")
            messages.append(message)
        
        return messages
    
    async def on_next_turn(self,game:"Game",action:dict,player_id:str):
        messages=[]
        if not game.check_is_turn_player_command(player_id):
            message=game.create_message("Not Your Turn",None)
            messages.append(message)
            return messages
        
        next_player=await game.start_next_turn()
        
        message1=game.create_message(None,f"Next Is Player {next_player}'s Turn")
        messages.append(message1)
        message2=game.create_message(None,"In Start Phase")
        message2["player_id"]=game.turn_player.player_id
        messages.append(message2)
        return messages