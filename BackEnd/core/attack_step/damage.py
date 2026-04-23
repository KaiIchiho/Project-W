from core.attack_step.attack_step_base import AttackStep
from core.attack_step.battle import Battle
from core.attack_type import AttackType
from typing import TYPE_CHECKING,Callable
if TYPE_CHECKING:
    from core.game import Game

class Damage(AttackStep):
    step_name="Damage"
    next_step=Battle
    def __init__(self,auto_next_step:Callable[[],None],attack_type:AttackType,stage_position_index:int):
        super().__init__(auto_next_step,attack_type,True,stage_position_index)
        
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)