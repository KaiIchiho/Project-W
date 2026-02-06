from models.player import Player
from core.sub_phase.phase_base import Phase
from core.attack_step import AttackStep
from typing import Callable,Optional
from core.sub_phase.stand_phase import StandPhase

class Game():
    FLOW_LOGS:list[str]=[]

    def __init__(self,
                 player_1:Optional[Player]=None,
                 player_2:Optional[Player]=None,
                 action_player:Optional[Player]=None
                 ):
        if player_1 is not None and player_2 is not None and player_1 is player_2:
            raise ValueError("2 Player Are the Same")
        self.player_1=player_1
        self.player_2=player_2
        
        self.action_player=action_player
        self.current_turn=0
        self.current_attack_step:AttackStep
        
        self.phase=StandPhase()
    
    def set_player_1(self,player_1:Player):
        if player_1 is not None:
            if player_1 is self.player_2:
                raise ValueError("2 Player Are the Same")
        self.player_1=player_1
    
    def set_player_2(self,player_2:Player):
        if player_2 is not None:
            if player_2 is self.player_1:
                raise ValueError("2 Player Are the Same")
        self.player_2=player_2
    
    def set_first_player(self,player:Player):
        self.action_player=player
        
    def set_player_to_none(self,player:Player)->int:
        if player is None:
            raise ValueError("None Player !")
        elif player is self.player_1 or player is self.player_2:
            raise ValueError("2 Player Are the Same")
        
        if self.player_1 is None:
            self.player_1=player
            return 1
        elif self.player_2 is None:
            self.player_2=player
            return 2
        else:
            return -1
        
    def start_turn(self):
        self.current_turn+=1
    
    def start_next_turn(self)->int:
        next_player=0
        if self.action_player is self.player_1:
            self.action_player=self.player_2
            next_player=2
        elif self.action_player is self.player_2:
            self.action_player=self.player_1
            next_player=1
        self.current_turn+=1
        return next_player
        
    def handle_action(self,action:dict)->str:
        log=self.phase.handle_action(self,action)
        if self.phase.is_complete:
            next_log=self.phase.on_next_phase(self,action)
            log=f"{log}\n{next_log}"
        return log