from core.attack_step.attack_step_base import AttackStep
from core.attack_step.trigger import Trigger
from core.attack_type import AttackType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class AttackDeclaration(AttackStep):
    def __init__(self,attack_type:AttackType):
        super().__init__(attack_type)
        self.next_step=Trigger
    
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)