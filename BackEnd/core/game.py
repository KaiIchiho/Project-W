from models.player import Player
from core.attack_step import AttackStep
from typing import Callable,Optional,Awaitable
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
        
        self.first_phase=StandPhase()
        self.phase=self.first_phase
    
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
        
    async def set_player_to_none(self,player:Player,callback:Optional[Callable[["Game",str],Awaitable[None]]]=None)->int:
        if player is None:
            raise ValueError("None Player !")
        elif player is self.player_1 or player is self.player_2:
            raise ValueError("2 Player Are the Same")
        
        if self.player_1 is None:
            self.player_1=player
            if callback is not None:
                await callback(self,player.player_id)
            return 1
        elif self.player_2 is None:
            self.player_2=player
            if callback is not None:
                await callback(self,player.player_id)
            return 2
        else:
            return -1
        
    def start_game(self):
        message={}
        if self.check_is_full_players()==False:
            return message
        self.current_turn=1
        message["room"]="Start Game"
        return message
    
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
    
    def reset_phase(self):
        self.phase=self.first_phase
        
    def handle_action(self,action:dict)->str:
        if self.check_is_full_players()==False:
            return "Game Is Not Players Full !"
        log=self.phase.handle_action(self,action)
        if self.phase.is_complete:
            next_log=self.phase.on_next_phase(self,action)
            log=f"{log}\n{next_log}"
        return log
    
    def check_is_full_players(self)->bool:
        if self.player_1 is None or self.player_2 is None:
            return False
        else:
            return True
    
    def check_command_player(self,user_id:str)->Player:
        if self.player_1 is None or self.player_2 is None:
            return None
        if self.player_1.player_id==user_id:
            return self.player_1
        elif self.player_2.player_id==user_id:
            return self.player_2
        else:
            return None
        
    def check_is_action_player_command(self,user_id:str)->bool:
        command_player=self.check_command_player(user_id)
        if command_player is None:
            return False
        if command_player is self.action_player:
            return True
        else:
            return False