from pydantic import BaseModel
from models.player import Player
from typing import Callable,Optional,Awaitable
from core.sub_phase.phase_base import Phase
from core.sub_phase.standby_phase import StandbyPhase
from core.sub_phase.stand_phase import StandPhase
from config import setting_ingame
from core.card_type import CardType
from models.playmat import StageStatus
# from models.card import Card
# from db import card_repo
# from schemas import object,common,game_flow
# from core.data_reader import DataReader

class Game():
    ws_send_message:Callable[[dict,str],Awaitable[None]]=None
    create_message:Callable[[int,str],dict]=None
    
    ws_send_data_to_user:Callable[[int,BaseModel],Awaitable[None]]
    ws_send_data_to_room:Callable[[int,BaseModel],Awaitable[None]]
    ws_send_data_to_room_except_target:Callable[[int,int,BaseModel],Awaitable[None]]
    
    phase:Optional[Phase]=None
    #attack_step:Optional[AttackStep]=None
    
    _is_in_progress=False
    
    def __init__(self,
                 room_id:int,
                 player_1:Optional[Player]=None,
                 player_2:Optional[Player]=None,
                 turn_player:Optional[Player]=None,
                 ):
        self.room_id=room_id
        
        if player_1 is not None and player_2 is not None and player_1 is player_2:
            raise ValueError("2 Player Are the Same")
        self.player_1=player_1
        self.player_2=player_2
        
        self.turn_player=turn_player
        self.current_turn=0
        #self.current_attack_step:AttackStep
        
        self.first_phase=StandbyPhase
        self.pre_turn_first_phase=StandPhase
    
    def set_player_1(self,player_1:Player):
        if player_1 is not None:
            if player_1 is self.player_2:
                raise ValueError("2 Player Are the Same.")
        self._set_player(1,player_1)
    
    def set_player_2(self,player_2:Player):
        if player_2 is not None:
            if player_2 is self.player_1:
                raise ValueError("2 Player Are the Same.")
        self._set_player(2,player_2)
    
    def _set_player(self,identity:int,player:Player):
        if identity==1 or identity==2:
            player.handle_level_up=self.handle_level_up
        if identity==1:
            self.player_1=player
        if identity==2:
            self.player_2=player
            
    async def auto_set_first_player(self):
        await self.set_first_player(self.player_1)
    
    async def set_first_player(self,player:Player):
        if player is not self.player_1 and player is not self.player_2:
            raise ValueError("Player is not in Game.")
        self.turn_player=player
        
    async def set_player_to_none(self,player:Player)->int:
        if player is None:
            raise ValueError("None Player !")
        elif player is self.player_1 or player is self.player_2:
            raise ValueError("2 Player Are the Same")
        
        result=-1
        if not player.check_has_deck():
            return result
        
        if self.player_1 is None:
            self.set_player_1(player)
            result=1
        elif self.player_2 is None:
            self.set_player_2(player)
            result=2
        
        return result
    
    def cancel_set_player(self,player_id:int)->int:
        result=-1
        if self._is_in_progress:
            return result
        if self.player_1 and self.player_1.player_id==player_id:
            self.player_1=None
            result=1
        elif self.player_2 and self.player_2.player_id==player_id:
            self.player_2=None
            result=2
        return result
    
    def get_is_in_progress(self)->bool:
        return self._is_in_progress
    
    async def start_game(
        self,player_id:int,
        start_game_callback:Callable[["Game",int],Awaitable[None]]=None
    ):
        if self.check_is_full_players()==False:
            return
        self._is_in_progress=True
        
        if start_game_callback:
            await start_game_callback(self,player_id)
        
        await self._in_start_phase()
    
    async def send_message(self,self_text:str,room_text:str,player_id:int):
        if self.create_message:
            message=self.create_message(self_text,room_text)
            await self.send_message_backage(message,player_id)
    
    async def send_message_backage(self,message:dict,player_id:int):
        if self.ws_send_message is not None:
            await self.ws_send_message(message,player_id)
    
    async def send_data_to_player(self,player_id:int,data:BaseModel):
        if self.ws_send_data_to_user:
            await self.ws_send_data_to_user(player_id,data)
    
    async def send_data_to_room(self,data:BaseModel):
        print("Log: send_data_to_room")
        if self.ws_send_data_to_room:
            await self.ws_send_data_to_room(self.room_id,data)
        else:
            print("Error: No ws_send_data_to_room")
    
    async def send_data_to_room_except_target(self,player_id:int,data:BaseModel):
        if self.ws_send_data_to_room_except_target:
            await self.ws_send_data_to_room_except_target(self.room_id,player_id,data)
    
    async def send_data_to_self_other(self,self_player_id:int,self_data:BaseModel,other_data:BaseModel):
        if not self.check_is_full_players():
            return
        self_identity=self.check_player_identity_by_id(self_player_id)
        other_player_id=-1
        if self_identity==-1:
            return
        elif self_identity==1:
            other_player_id=self.player_2.player_id
        elif self_identity==2:
            other_player_id=self.player_1.player_id
        await self.send_data_to_room_except_target(other_player_id,self_data)
        await self.send_data_to_player(other_player_id,other_data)
    
    async def _in_start_phase(self):
        self.phase=self.first_phase()
        await self.phase.on_enter(self)
    
    async def _in_turn_start_phase(self):
        self.phase=self.pre_turn_first_phase()
        await self.phase.on_enter(self)
    
    async def start_next_turn(
        self,
        player_id:int,
        is_switch_turn_player:bool=True,
        on_player_switch:Callable[["Game",int],Awaitable[None]]=None,
        in_turn_start_phase:Callable[[],None]=None
    )->int:
        print("Log: start_next_turn")
        if is_switch_turn_player:
            if self.turn_player is self.player_1:
                self.turn_player=self.player_2
            elif self.turn_player is self.player_2:
                self.turn_player=self.player_1
        self.current_turn+=1
        
        if on_player_switch is not None:
            await on_player_switch(self,player_id)
        
        await self._in_turn_start_phase()
        if in_turn_start_phase is not None:
            in_turn_start_phase()
    
    def init_players_playmat(self)->bool:
        if not self.check_is_full_players():
            return False
        result_1=self.player_1.init_playmat()
        result_2=self.player_2.init_playmat()
        return result_1,result_2
    
    def player_deck_shuffle(self,player_id:int)->bool:
        player_identity=self.check_player_identity_by_id(player_id)
        result=False
        player=None
        if player_identity==1 and self.player_1:
            player=self.player_1
        elif player_identity==2 and self.player_2:
            player=self.player_2
        
        if player:
            result=player.deck_shuffle()
        return result
    
    async def handle_action(self,action:dict,event:str,player_id:int):
        if self.check_is_full_players()==False:
            await self.send_message("Game Is Not Players Full !",None,None)
            return
        
        await self.phase.handle_action(self,action,event,player_id)
        
        if self.phase.is_complete:
            await self.phase.on_next_phase(self,action,self.get_turn_player_id())
    
    async def handle_level_up(self,player_id:int):
        if self.phase:
            await self.phase.start_level_up(self,player_id)
    
    def draw_initial_hand(self,player_id:int)->bool:
        player=self._get_ingame_player_by_id(player_id)
        if not player:
            return False
        for i in range(setting_ingame.INITIAL_HAND):
            player.draw()
        return True
    
    def player_all_stage_rest_stand(self,player_id:int)->bool:
        player=self.check_command_player(player_id)
        if not player:
            return False
        
        player.all_stage_rest_stand()
        return True
    
    def player_draw(self,player_id:int)->int:
        identity=self.check_player_identity_by_id(player_id)
        card_id=-1
        if identity==1:
            card_id=self.player_1.draw()
        elif identity==2:
            card_id=self.player_2.draw()
        return card_id
    
    def turn_player_draw(self)->int:
        player=self.turn_player
        card_id=-1
        if player:
            card_id=player.draw()
        return card_id
    
    def swap_hand_cards(self,player_id:int,hand_index_list:list[int]):
        player:Player=self.check_command_player(player_id)
        identity=self.check_player_identity(player)
        success=False
        if player:
            if identity==2 and not self.player_1.get_is_swap_hand():
                success=False
            else:
                success=player.swap_hand_cards(hand_index_list)
        
        return success,identity
    
    async def transition_to_next_phase(
        self,player_id:int,send_data_callback:Callable[["Game",int,bool],Awaitable[None]]
    ):
        print(f"Log: on_next_phase, Now Phase Is {self.phase.phase_name}")
        if self.phase.is_frozen():
            return
        await self.phase.on_exit(self)
        _is_next_phase=False
        if self.phase.next_phase is None:
            _is_next_phase=False
        else:
            _is_next_phase=True
        
        if send_data_callback:
            await send_data_callback(self,player_id,_is_next_phase)
        
        if _is_next_phase:
            self.phase=self.phase.next_phase()
            await self.phase.on_enter(self)
    
    async def player_hand_to_clock(
        self,player_id:int,hand_index:int,
        clock_set_callback:Callable[[int],Awaitable[None]]=None
    ):
        card_id=-1
        player=self.check_command_player(player_id)
        if not player:
            if clock_set_callback:
                await clock_set_callback(card_id)
            return card_id
        card=player.remove_hand(hand_index)
        if card:
            await player.set_card_to_clock(card,clock_set_callback)
            card_id=card.card_id
        else:
            if clock_set_callback:
                await clock_set_callback(card_id)
        return card_id
    
    def play_char_card(self,player_id:int,hand_index:int,stage_index:int):
        player=self.check_command_player(player_id)
        has_card=player.check_has_stage_card(stage_index)
        
        card_type=player.read_hand_type(hand_index)
        if card_type!=CardType.CH:
            return has_card,False
        
        card=player.pop_hand(hand_index)
        result=player.set_card_to_stage(card,stage_index)
        return has_card,result
    
    def play_event_card(self,player_id:int,hand_index)->bool:
        player=self.check_command_player(player_id)
        
        card_type=player.read_hand_type(hand_index)
        if card_type!=CardType.EV:
            return False
        
        card=player.pop_hand(hand_index)
        result=player.set_card_to_resolution(card)
        return result
    
    def move_stage_char(self,player_id:int,ori_index:int,tar_index:int):
        player=self.check_command_player(player_id)
        if not player:
            return False,None,None,None,None,None,None
        return player.move_stage_char(ori_index,tar_index)
    
    def set_cx_card(self,player_id:int,hand_index:int):
        player=self.check_command_player(player_id)
        card_type=player.read_hand_type(hand_index)
        print(f"Log: Set CX Card. Card Type: {card_type.value}")
        has_set_cx=player.check_has_set_cx()
        if card_type!=CardType.CX:
            return False,has_set_cx
        card=player.pop_hand(hand_index)
        player.set_cx(card)
        return True,has_set_cx
    
    def remove_cx_card(self,player_id:int)->bool:
        player=self.check_command_player(player_id)
        has_set_cx=player.check_has_set_cx()
        player.remove_cx()
        return has_set_cx
    
    def remove_stage_char_to_waiting_room(self,player_id:int,stage_index:int)->bool:
        player=self.check_command_player(player_id)
        return player.remove_stage_to_waiting_room(stage_index)
    
    def get_hand_exceed_limit(self,player_id:int)->bool:
        player=self.check_command_player(player_id)
        return player.get_hand_exceed_limit()
    
    def discard_hand(self,player_id:int,hand_index:int)->bool:
        player=self.check_command_player(player_id)
        card=player.pop_hand(hand_index)
        return player.set_card_to_waiting_room(card)
    def discard_hand_by_list(self,player_id:int,hand_index_list:list[int]):
        hand_index_list_cp=sorted(hand_index_list,reverse=True)
        print("Log: discard_hand_by_list")
        print(f"Log: hand_index_list: {hand_index_list}")
        print(f"Log: hand_index_list_cp: {hand_index_list_cp}")
        
        for index in hand_index_list_cp:
            if not self.discard_hand(player_id,index):
                return False
            
        return True
    
    def get_current_turn_num(self)->int:
        return self.current_turn
    
    def get_player_stage_info(self,player_id:int,stage_index:int,info_list:list=[])->dict:
        player=self.check_command_player(player_id)
        info_dict=player.get_stage_cards_info_by_list(info_list)[stage_index]
        return info_dict
    
    def get_player_stage_owner_id(self,player_id:int,stage_index:int)->int:
        player=self.check_command_player(player_id)
        return player.get_stage_card_owner_id(stage_index)
    
    def get_player_stage_status(self,player_id:int,stage_index:int)->StageStatus:
        player=self.check_command_player(player_id)
        return player.get_stage_card_status(stage_index)
    
    def set_player_stage_status(self,player_id:int,stage_index:int,status:StageStatus)->bool:
        player=self.check_command_player(player_id)
        return player.set_stage_status(stage_index,status)
    
    def set_player_stage_reverse(self,player_id:int,stage_index:int)->bool:
        return self.set_player_stage_status(player_id,stage_index,StageStatus.REVERSE)
    
    def set_player_stage_rest(self,player_id:int,stage_index:int)->bool:
        return self.set_player_stage_status(player_id,stage_index,StageStatus.REST)
    
    def get_player_stage_index_by_status(self,player_id:int,status:StageStatus)->list[int]:
        player=self.check_command_player(player_id)
        return player.get_stage_index_by_status(status)
    
    def get_player_stage_reverse_index(self,player_id:int)->list[int]:
        return self.get_player_stage_index_by_status(player_id,StageStatus.REVERSE)
    
    def get_player_stage_rest_index(self,player_id:int)->list[int]:
        return self.get_player_stage_index_by_status(player_id,StageStatus.REST)
    
    def get_player_stage_stand_index(self,player_id:int)->list[int]:
        return self.get_player_stage_index_by_status(player_id,StageStatus.STAND)
    
    def get_other_player_stage_is_empty(self,self_player_id:int,self_stage_index:int)->bool:
        other_player=self.check_command_other_player(self_player_id)
        other_stage_index=self.get_other_stage_index(self_stage_index)
        is_empty=not other_player.check_has_stage_card(other_stage_index)
        return is_empty
    
    def get_other_player_stage_info(self,self_player_id:int,self_stage_index:int,info_list:list=[]):
        other_player=self.check_command_other_player(self_player_id)
        other_stage_index=self.get_other_stage_index(self_stage_index)
        is_empty=not other_player.check_has_stage_card(other_stage_index)
        info_dict=other_player.get_stage_cards_info_by_list(info_list)[other_stage_index]
        return other_stage_index,is_empty,info_dict
    
    def get_other_stage_index(self,self_stage_index:int)->int:
        front_index_list=setting_ingame.FRONT_STAGE
        back_index_list=setting_ingame.BACK_STAGE
        index_list:list
        try:
            idx=front_index_list.index(self_stage_index)
            index_list=front_index_list
        except ValueError:
            try:
                idx=back_index_list.index(self_stage_index)
                index_list=back_index_list
            except ValueError:
                raise ValueError(f"Stage Index {self_stage_index} Invalid")
        other_idx=len(index_list)-idx-1
        other_stage_index=index_list[other_idx]
        return other_stage_index
    
    def player_has_stage_card(self,player_id:int,stage_index:int)->bool:
        player=self.check_command_player(player_id)
        return player.check_has_stage_card(stage_index)
    
    def player_check_trigger(self,player_id:int):
        player=self.check_command_player(player_id)
        checked_card=player.flip_over_deck_one_card()
        card_id=checked_card.card_id
        triggers=checked_card.get_triggers()
        player.set_card_to_resolution(checked_card)
        return card_id,triggers
    
    def player_check_damage(self,player_id:int,times:int,info_list:list):
        player=self.check_command_player(player_id)
        checked_card_info=[]
        is_broken=False
        for i in range(times):
            checked_card=player.flip_over_deck_one_card()
            card_info=checked_card.get_current_info_by_list(info_list)
            checked_card_info.append(card_info)
            card_type=checked_card.get_card_type()
            player.set_card_to_resolution(checked_card)
            if card_type==CardType.CX:
                is_broken=True
                break
        return is_broken,checked_card_info
    
    # 解決領域のカードを処理することを始める
    # 戻り値：中断フラグ
    async def player_start_handle_resolution(self,player_id:int,target:str)->bool:
        player=self.check_command_player(player_id)
        flag=await player.start_handle_resolution(target)
        return flag
    # 解決領域のカードを処理することを続ける
    # keyは存在する場合、処理中のtargetと対応しなければ動かない
    # keyは存在しない場合普通に動く
    # 戻り値：中断フラグ
    async def player_continue_handle_resolution(self,player_id:int,key:str="")->bool:
        player=self.check_command_player(player_id)
        flag=await player.continue_handle_resolution(key)
        return flag
    
    def player_process_level_up(self,player_id:int,clock_index:int)->bool:
        player=self.check_command_player(player_id)
        return player.process_level_up(clock_index)
    
    def check_is_first_phase(self)->bool:
        return isinstance(self.phase,self.first_phase)
    
    def check_player_identity(self,user:Player)->int:
        if self.player_1 is user:
            return 1
        elif self.player_2 is user:
            return 2
        else:
            return -1
    
    def check_player_identity_by_id(self,player_id:int)->int:
        # player=None
        if self.player_1 and self.player_1.player_id==player_id:
            return 1
        elif self.player_2 and self.player_2.player_id==player_id:
            return 2
        else:
            return -1
    
    def check_turn_player_identity(self)->int:
        return self.check_player_identity(self.turn_player)
    
    def check_is_full_players(self)->bool:
        if self.player_1 is None or self.player_2 is None:
            return False
        else:
            return True
    
    def check_command_player(self,player_id:int)->Player:
        # if self.player_1 is None or self.player_2 is None:
        #     return None
        if self.player_1 and self.player_1.player_id==player_id:
            return self.player_1
        elif self.player_2 and self.player_2.player_id==player_id:
            return self.player_2
        else:
            return None
    
    def check_command_other_player(self,player_id:int)->Player:
        if self.player_1 and self.player_1.player_id==player_id:
            return self.player_2
        elif self.player_2 and self.player_2.player_id==player_id:
            return self.player_1
        else:
            return None
    
    def check_is_turn_player_command(self,player_id:int)->bool:
        print(f"Check is Action Player ID: {player_id}")
        command_player=self.check_command_player(player_id)
        if command_player is None:
            print(f"Check is Action Player None")
            return False
        print(f"Command Player ID: {command_player.player_id}")
        print(f"Action Player ID: {self.turn_player.player_id}")
        if command_player is self.turn_player:
            print(f"Check is Action Player True")
            return True
        else:
            print(f"Check is Action Player False")
            return False
    
    def _get_ingame_player_by_id(self,player_id:int)->Player:
        if self.player_1 and self.player_1.player_id==player_id:
            return self.player_1
        elif self.player_2 and self.player_2.player_id==player_id:
            return self.player_2
        else:
            return None
    
    def get_player_name_by_id(self,player_id:int)->str:
        if self.player_1 and self.player_1.player_id==player_id:
            return self.player_1.name
        elif self.player_2 and self.player_2.player_id==player_id:
            return self.player_2.name
        else:
            return ""
    
    def get_turn_player_id(self)->int:
        if self.turn_player:
            return self.turn_player.player_id
        else:
            return -1
    
    def get_turn_player_name(self)->str:
        if self.turn_player:
            return self.turn_player.name
        else:
            return ""
        
    def get_other_player_id(self)->int:
        if not self.check_is_full_players():
            return -1
        if not self.turn_player:
            return -1
        elif self.turn_player is self.player_1:
            return self.player_2.player_id
        elif self.turn_player is self.player_2:
            return self.player_1.player_id
    
    def get_other_player_name(self)->str:
        if not self.check_is_full_players():
            return ""
        if not self.turn_player:
            return ""
        elif self.turn_player is self.player_1:
            return self.player_2.name
        elif self.turn_player is self.player_2:
            return self.player_1.name
    
    def check_stage_state(self,player_id:int,stage_index:int)->bool:
        player=self.check_command_player(player_id)
        stage=player.playmat.stage[stage_index]
        if stage is None:
            return False
        else:
            return True
    
    async def forced_game_end(self):
        self._is_in_progress=False
        
        print("Log: forced game end.")
        if not self.ws_send_message:
            return
        
        player_id=""
        if self.player_1:
            player_id=self.player_1.player_id
        elif self.player_2:
            player_id=self.player_2.player_id
        
        if self.create_message:
            await self.ws_send_message(self.create_message(None,"Game End"),player_id)