from core.state_machine_base import StateMachine
from core.attack_type import AttackType
from schemas import game_flow
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class AttackStep(StateMachine):
    step_name="Attack Step Base"
    next_step=None
    is_complete=False
    is_declarated=False
    handlers={
        "next_step":"on_next_step"
    }
    def __init__(self,attack_type:AttackType,is_declarated:bool):
        self.attack_type=attack_type
        self.is_declarated=is_declarated
        
    def __init_subclass__(cls, **kwargs):
        super.__init_subclass__(**kwargs)
        cls.handlers=cls.handlers.copy()
    
    async def on_enter(self,game:"Game"):
        print(f"Log: Attack Step: {self.step_name} On Enter")
    async def on_exit(self,game:"Game"):
        print(f"Log: Attack Step: {self.step_name} On Exit")
    
    async def on_next_step(self,game:"Game",action:dict,player_id:str):
        # if game.attack_step:
        #     game.attack_step.on_exit()
        # if not self.next_step:
        #     game.attack_step=None
        #     return
        # game.attack_step=self.next_step()
        pass