from enum import Enum,auto

class AttackStep(Enum):
    ATTACK_DECLARATION=auto()
    TRIGGER=auto()
    DAMAGE=auto()
    BATTLE=auto()
    ENCORE=auto()