from core.attack_step.attack_step_base import AttackStep
from core.attack_step.damage import Damage
from core.attack_type import AttackType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class Trigger(AttackStep):
    step_name="Trigger"
    next_step=Damage
    def __init__(self,attack_type:AttackType,is_declarated:bool):
        super().__init__(attack_type,is_declarated)
        
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)