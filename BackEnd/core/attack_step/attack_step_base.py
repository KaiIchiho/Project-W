from core.attack_type import AttackType
from schemas import game_flow
from services.parse_model import parse_model
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class AttackStep:
    step_name="Attack Step Base"
    next_step=None
    is_complete=False
    handlers={
        "next_step":"on_next_step"
    }
    def __init__(self,attack_type:AttackType):
        self.attack_type=attack_type
        
    def __init_subclass__(cls, **kwargs):
        super.__init_subclass__(**kwargs)
        cls.handlers=cls.handlers.copy()
    
    async def on_enter(self,game:"Game"):
        print(f"Log: Attack Step: {self.step_name} On Enter")
    async def on_exit(self,game:"Game"):
        print(f"Log: Attack Step: {self.step_name} On Exit")
    
    # async def handle_action(self,game:"Game",action:dict,player_id:str):
    #     handle_name=self.handlers.get(action.get("action"))
    #     if not handle_name:
    #         return
    #     handler=getattr(self,handle_name)
        
    #     await handler(game,action,player_id)
    
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
    
    async def on_next_step(self,game:"Game",action:dict,player_id:str):
        # if game.attack_step:
        #     game.attack_step.on_exit()
        # if not self.next_step:
        #     game.attack_step=None
        #     return
        # game.attack_step=self.next_step()
        pass