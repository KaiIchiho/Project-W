from core.attack_step.attack_step_base import AttackStep
from core.attack_step.damage import Damage
from core.attack_type import AttackType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class Counter(AttackStep):
    step_name="Counter"
    next_step=Damage
    def __init__(self,attack_type:AttackType,stage_position_index:int):
        super().__init__(attack_type,True,stage_position_index)
        
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)