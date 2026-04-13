from schemas import event_type,game_flow
from services.sub_command.next_turn_command import NextTurnCommand
from services.parse_model import parse_model
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class Phase:
    handlers={
        event_type.NEXT_PHASE:"on_next_phase",
        event_type.NEXT_TURN:"on_next_turn"
        }
    is_complete=False
    phase_name="phase_base"
    next_phase=None
    
    def __init_subclass__(cls, **kwargs):
        super.__init_subclass__(**kwargs)
        cls.handlers=cls.handlers.copy()
    
    async def on_enter(self,game:"Game"):
        await game.phase_enter_response()
        # await game.send_message(None,f"Enter {self.phase_name}",game.turn_player.player_id)
        # return self.phase_name
    async def on_exit(self,game:"Game"):
        await game.phase_exit_response()
        # await game.send_message(None,f"Exit {self.phase_name}",game.turn_player.player_id)
        # return self.phase_name
    
    async def send_message_list(self,game:"Game",message_list:list[dict],default_player_id:int):
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
    
    async def handle_action(self,game:"Game",action:dict,event:str,player_id:int):
        model,req=self.parse_action_model(action,event)
        if not model or not req:
            return
        
        handler_name=self.handlers.get(event)
        if not handler_name:
            raise ValueError("Action Not Found")
        handler=getattr(self,handler_name)
        
        await handler(game,req,player_id)
        # messages=await handler(game,req,player_id)
        
        # await self.send_message_list(game,messages,player_id)
    
    async def on_next_phase(self,game:"Game",req:game_flow.NextPhaseRequest,player_id:int):
        if not game.check_is_turn_player_command(player_id):
            return
        game.transition_to_next_phase(player_id)
    # )->list[dict]:
        # pass
        # messages=[]
        # if not game.check_is_turn_player_command(player_id):
        #     message=game.create_message("Not Your Turn",None)
        #     messages.append(message)
        #     return messages
        
        # print(f"Log: on_next_phase, Now Phase Is {self.phase_name}")
        # await game.phase.on_exit(game)
        # if self.next_phase is None:
        #     print("Log: on_next_phase, Next Phase Is None")
        #     messages=await self.on_next_turn(game,action,player_id)
        # else:
        #     print("Log: on_next_phase, Next Phase Is Not None")
        #     game.phase=self.next_phase()
        #     await game.phase.on_enter(game)
        #     message=game.create_message(None,f"Next Phase : {game.phase.phase_name}")
        #     messages.append(message)
        
        # return messages
    
    async def on_next_turn(self,game:"Game",req:game_flow.NextTurnRequest,player_id:int)->list[dict]:
        # messages=[]
        if not game.check_is_turn_player_command(player_id):
            # message=game.create_message("Not Your Turn",None)
            # messages.append(message)
            # return messages
            return
        
        await game.start_next_turn(player_id)
        # next_player=await game.start_next_turn()
        
        # message1=game.create_message(None,f"Next Is Player {next_player}'s Turn")
        # messages.append(message1)
        # message2=game.create_message(None,"In Start Phase")
        # message2["player_id"]=game.turn_player.player_id
        # messages.append(message2)
        # return messages
    
    def parse_action_model(self,action:dict,event:str):
        model=game_flow.event_req.get(event)
        if model is None:
            return None,None
        req=parse_model(action,model)
        return model,req
        