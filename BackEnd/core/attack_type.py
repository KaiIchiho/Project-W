from enum import Enum
# from typing import TYPE_CHECKING
# if TYPE_CHECKING

class AttackType(str,Enum):
    DIRECT="direct"
    FRONT="front"
    SIDE="side"
    
    @staticmethod
    def check_could_attack(attack_type:"AttackType",other_is_empty:bool)->bool:
        could_when_is_empty=attack_type_empty_registry.get(attack_type)
        if could_when_is_empty is None:
            return False
        return could_when_is_empty==other_is_empty

attack_type_empty_registry={
    AttackType.DIRECT:True,
    AttackType.FRONT:False,
    AttackType.SIDE:False
}