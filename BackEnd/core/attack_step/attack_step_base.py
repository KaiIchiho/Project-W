from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class AttackStep:
    step_name="Attack Step Base"
    next_step=None
    handlers={
        "next_step":"on_next_step"
        }
    is_complete=False
    
    async def on_enter(self,game:"Game"):
        pass
    async def on_exit(self,game:"Game"):
        pass
    
    async def handle_action(self,game:"Game",action:dict,player_id:str):
        handle_name=self.handlers.get(action.get("action"))
        if not handle_name:
            return
        handler=getattr(self,handle_name)
        
        await handler(game,action,player_id)
        
    async def on_next_step(self,game:"Game",action:dict,player_id:str):
        if game.attack_step:
            game.attack_step.on_exit()
        if not self.next_step:
            game.attack_step=None
            return
        game.attack_step=self.next_step()