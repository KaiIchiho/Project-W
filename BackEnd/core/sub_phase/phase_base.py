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
    async def on_exit(self,game:"Game"):
        await game.phase_exit_response()
    
    async def handle_action(self,game:"Game",action:dict,event:str,player_id:int):
        model,req=self.parse_action_model(action,event)
        if not model or not req:
            return
        
        handler_name=self.handlers.get(event)
        if not handler_name:
            # raise ValueError("Action Not Found")
            print(f"Action {handler_name} Not Found")
            return
        
        handler=getattr(self,handler_name)
        await handler(game,req,player_id)
        
    async def on_next_phase(self,game:"Game",req:game_flow.NextPhaseRequest,player_id:int):
        print("Log: on_next_phase")
        if not game.check_is_turn_player_command(player_id):
            return
        await game.transition_to_next_phase(player_id)
    
    async def on_next_turn(self,game:"Game",req:game_flow.NextTurnRequest,player_id:int):
        if not game.check_is_turn_player_command(player_id):
            return
        
        await game.start_next_turn(player_id)
    
    def parse_action_model(self,action:dict,event:str):
        model=game_flow.event_req.get(event)
        if model is None:
            return None,None
        req=parse_model(action,model)
        return model,req
    
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