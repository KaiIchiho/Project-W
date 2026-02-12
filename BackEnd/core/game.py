from models.player import Player
from core.attack_step import AttackStep
from typing import Callable,Optional,Awaitable
from core.sub_phase.phase_base import Phase
from core.sub_phase.stand_phase import StandPhase

class Game():
    ws_send_message:Callable[[dict,str],Awaitable[None]]=None
    
    phase:Optional[Phase]=None

    def __init__(self,
                 player_1:Optional[Player]=None,
                 player_2:Optional[Player]=None,
                 action_player:Optional[Player]=None,
                 ws_send_message:Optional[Callable[[dict,str],Awaitable[None]]]=None
                 ):
        if player_1 is not None and player_2 is not None and player_1 is player_2:
            raise ValueError("2 Player Are the Same")
        self.player_1=player_1
        self.player_2=player_2
        
        self.action_player=action_player
        self.current_turn=0
        self.current_attack_step:AttackStep
        
        self.first_phase=StandPhase()
        
        self.ws_send_message=ws_send_message
    
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
        
    async def set_player_to_none(self,player:Player,callback:Optional[Callable[[str],Awaitable[None]]]=None)->int:
        if player is None:
            raise ValueError("None Player !")
        elif player is self.player_1 or player is self.player_2:
            raise ValueError("2 Player Are the Same")
        
        if self.player_1 is None:
            self.player_1=player
            #if self.ws_send_message is not None:
            await self.send_message(
                "Standby Succeeded !",
                "Player 1 Standby",
                player.player_id)
            if callback is not None:
                await callback(player.player_id)
            return 1
        elif self.player_2 is None:
            self.player_2=player
            #if self.ws_send_message is not None:
            await self.send_message(
                "Standby Succeeded !",
                "Player 2 Standby",
                player.player_id)
            if callback is not None:
                await callback(player.player_id)
            return 2
        else:
            #if self.ws_send_message is not None:
            await self.send_message(
                "Standby Failed !",
                None,
                player.player_id)
            return -1
        
    async def start_game(self,player_id:str):
        if self.check_is_full_players()==False:
            return
        self.current_turn=1
        self.set_first_player(self.player_1)
        await self.send_message(None,"Start Game",player_id)
        self.__in_start_phase()
    
    def create_message(self,self_text:str,room_text:str)->dict:
        message={}
        message["self"]=self_text
        message["room"]=room_text
        return message
    
    async def send_message(self,self_text:str,room_text:str,player_id:str):
        message=self.create_message(self_text,room_text)
        await self.send_message_backage(message,player_id)
    
    async def send_message_backage(self,message:dict,player_id:str):
        if self.ws_send_message is not None:
            await self.ws_send_message(message,player_id)
    
    def __in_start_phase(self):
        self.phase=self.first_phase
        self.phase.on_enter(self)
    
    def start_next_turn(self)->int:
        next_player=0
        if self.action_player is self.player_1:
            self.action_player=self.player_2
            next_player=2
        elif self.action_player is self.player_2:
            self.action_player=self.player_1
            next_player=1
        self.current_turn+=1
        self.__in_start_phase()
        
        return next_player
    
    def reset_phase(self):
        self.phase=self.first_phase
        
    async def handle_action(self,action:dict,player_id:str):
        if self.check_is_full_players()==False:
            await self.send_message("Game Is Not Players Full !",None,None)
            return
        
        message=self.phase.handle_action(self,action,player_id)
        await self.send_message_backage(message,player_id)
        
        if self.phase.is_complete:
            next_message=self.phase.on_next_phase(self,action)
            #log=f"{log}\n{next_log}"
            await self.send_message_backage(next_message,player_id)
    
    def check_player_identity(self,user:Player)->int:
        if self.player_1 is user:
            return 1
        elif self.player_2 is user:
            return 2
        else:
            return -1
    
    def check_player_identity_by_id(self,player_id:str)->int:
        player=self.check_command_player(player_id)
        return self.check_player_identity(player)
    
    def check_is_full_players(self)->bool:
        if self.player_1 is None or self.player_2 is None:
            return False
        else:
            return True
    
    def check_command_player(self,player_id:str)->Player:
        if self.player_1 is None or self.player_2 is None:
            return None
        print(f"player 1 ID: {self.player_1.player_id}")
        print(f"player 2 ID: {self.player_2.player_id}")
        print(f"checked player ID: {player_id}")
        if self.player_1.player_id==player_id:
            return self.player_1
        elif self.player_2.player_id==player_id:
            return self.player_2
        else:
            return None
        
    def check_is_action_player_command(self,player_id:str)->bool:
        print(f"Check is Action Player ID: {player_id}")
        command_player=self.check_command_player(player_id)
        if command_player is None:
            print(f"Check is Action Player None")
            return False
        print(f"Command Player ID: {command_player.player_id}")
        print(f"Action Player ID: {self.action_player.player_id}")
        if command_player is self.action_player:
            print(f"Check is Action Player True")
            return True
        else:
            print(f"Check is Action Player False")
            return False