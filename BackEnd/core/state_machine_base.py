from schemas import game_flow
from services.parse_model import parse_model

class StateMachine():
    async def handle_action(self,game:"Game",action:dict,event:str,player_id:int):
        model,req=self.parse_action_model(action,event)
        if not model or not req:
            return False
        
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