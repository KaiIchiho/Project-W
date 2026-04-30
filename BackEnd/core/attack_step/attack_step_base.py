from core.state_machine_base import StateMachine
from core.attack_type import AttackType
from schemas import game_flow
from typing import TYPE_CHECKING,Type,Callable,Awaitable
if TYPE_CHECKING:
    from core.game import Game

class AttackStep(StateMachine):
    step_name="Attack Step Base"
    next_step:Type["AttackStep"]=None
    is_complete=False
    is_declarated=False
    handlers={
        "next_step":"on_next_step"
    }
    stage_position_index:int=-1
    auto_next_step:Callable[["Game"],Awaitable[None]]=None
    def __init__(
        self,auto_next_step:Callable[["Game"],Awaitable[None]],attack_type:AttackType,is_declarated:bool,stage_position_index:int=-1
    ):
        self.auto_next_step=auto_next_step
        self.attack_type=attack_type
        self.is_declarated=is_declarated
        self.stage_position_index=stage_position_index
        
    def __init_subclass__(cls, **kwargs):
        super.__init_subclass__(**kwargs)
        cls.handlers=cls.handlers.copy()
    
    async def on_enter(self,game:"Game"):
        print(f"Log: Attack Step: {self.step_name} On Enter")
    async def on_exit(self,game:"Game"):
        print(f"Log: Attack Step: {self.step_name} On Exit")
    
    async def on_next_step(self,game:"Game"):
        if self.auto_next_step:
            await self.auto_next_step(game)