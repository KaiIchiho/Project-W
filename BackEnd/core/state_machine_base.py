from schemas import game_flow
from services.parse_model import parse_model
from typing import TYPE_CHECKING
import asyncio
if TYPE_CHECKING:
    from core.game import Game

class StateMachine():
    def __init__(self):
        self.waiting_for = {
            "type": "",
            "player_id":-1
        }
        self._wait_event = asyncio.Event()
    
    async def handle_action(self,game:"Game",action:dict,event:str,player_id:int):
        model,req=self.parse_action_model(action,event)
        if not model or not req:
            return False
        
        if not self.match_expected_action(event,player_id):
            print("Log: CANNOT match_expected_action")
            return False
        else:
            print("Log: CAN match_expected_action")
            self._clear_waiting_event()
            self._wait_event.set()
            print("Log: Set Event")
        
        handler_name=self.handlers.get(event)
        if not handler_name:
            print(f"Action {handler_name} Not Found")
            return False
        
        print(f"Log: handler action name: {handler_name}")
        handler=getattr(self,handler_name)
        await handler(game,req,player_id)
        return True
    
    def parse_action_model(self,action:dict,event:str):
        model=game_flow.event_req.get(event)
        if model is None:
            return None,None
        req=parse_model(action,model)
        return model,req
    
    async def _wait_event(self):
        self._wait_event.clear()
        print("Log: Clear Event")
        await self._wait_event
        print("Log: Wait Event")
    
    def set_waiting_event(self,type:str,player_id:int):
        if not type:
            raise ValueError("Set Waiting Event is Invalid")
        print("Log: set_waiting_event")
        self.waiting_for["type"]=type
        self.waiting_for["player_id"]=player_id
        print(self.waiting_for)
    
    def _clear_waiting_event(self):
        print("Log: clear_waiting_event")
        self.waiting_for["type"]=""
        self.waiting_for["player_id"]=-1
        print(self.waiting_for)
    
    def match_expected_action(self,type:str,player_id:int)->bool:
        print("Log: match_expected_action")
        print(self.waiting_for)
        current_type=self.waiting_for.get("type")
        current_player_id=self.waiting_for.get("player_id")
        if not current_type:
            return True
        elif current_type==type and current_player_id==player_id:
                return True
        else:
            return False