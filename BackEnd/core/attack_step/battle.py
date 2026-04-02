from core.attack_step.attack_step_base import AttackStep
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class Battle(AttackStep):
    async def __init__(self):
        super().__init__()
        self.next_step=None
        
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)