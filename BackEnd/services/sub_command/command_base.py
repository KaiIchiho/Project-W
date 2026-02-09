#from enum import Enum

#class Command(Enum):
#    STANDBY="standby"
#    NEXT_PHASE="next_phase"
#    NEXT_TURN="next_turn"
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class Command:
    def execute(self,game:"Game"):
        pass