from models.base import GameObject
from models.card import Card
from models.deck import Deck
from models.playmat import Playmat
from core.card_type import CardType
from config import setting_ingame
from models.playmat import StageStatus
from typing import Callable,Awaitable

class Player(GameObject):
    handle_level_up:Callable[[int],Awaitable[None]]=None
    on_defeat:Callable[[int],Awaitable[None]]=None
    
    FLAG_CALLBACK_REGISTRY:dict={
        "clock":"handle_level_up"
    }
    
    def __init__(self,
                 player_id:int,
                 name:str,
                 playmat:Playmat=None
                 ):
        super().__init__(player_id)
        self._deck_id:int=-1
        self.player_id=player_id
        self.name=name
        self.playmat=playmat
        self.hand:list[Card]=[]
        
        self._is_swap_hand:bool=False
    
    def set_deck_id(self,deck_id:int)->bool:
        self._deck_id=deck_id
        return True
    
    def get_deck_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        if self.playmat:
            return self.playmat.get_deck_cards_info_by_list(card_info_list)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    def get_stage_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        if self.playmat:
            return self.playmat.get_stage_cards_info_by_list(card_info_list)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    def get_marker_cards_info_by_list(self,card_info_list:list[str])->list[list[dict]]:
        if self.playmat:
            return self.playmat.get_marker_cards_info_by_list(card_info_list)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    def get_waiting_room_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        if self.playmat:
            return self.playmat.get_waiting_room_cards_info_by_list(card_info_list)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    def get_hand_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        cards_info=[]
        for card in self.hand:
            if card is None:
                continue
            card_info=card.get_current_info_by_list(card_info_list)
            cards_info.append(card_info)
        return cards_info
    def get_clock_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        if self.playmat:
            return self.playmat.get_clock_cards_info_by_list(card_info_list)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    def get_level_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        if self.playmat:
            return self.playmat.get_level_cards_info_by_list(card_info_list)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    def get_stock_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        if self.playmat:
            return self.playmat.get_stock_cards_info_by_list(card_info_list)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    def get_climax_id(self)->int:
        if self.playmat:
            return self.playmat.get_climax_id()
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    def get_climax_card_info_by_list(self,card_info_list:list[str])->dict:
        if self.playmat:
            return self.playmat.get_climax_card_info_by_list(card_info_list)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    def get_memory_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        if self.playmat:
            return self.playmat.get_memory_cards_info_by_list(card_info_list)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    def get_resolution_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        if self.playmat:
            return self.playmat.get_resolution_cards_info_by_list(card_info_list)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    
    def check_has_deck(self)->bool:
        if self._deck_id==-1:
            return False
        else:
            return True
    
    def init_playmat(self)->bool:
        self.playmat=Playmat(self.ori_owner_id)
        deck=Deck(self.ori_owner_id)
        if not deck.init_deck_by_deck_id(self._deck_id):
            return False
        self.playmat.set_init_deck(deck)
        # self.playmat.deck_shuffle()
        return True
    
    def deck_shuffle(self)->bool:
        if self.playmat:
            self.playmat.deck_shuffle()
            return True
        else:
            return False
    
    def draw(self)->int:
        print(f"{self.name} Draw")
        draw_card=self.playmat.deck.draw()
        self.hand.append(draw_card)
        return draw_card.card_id
        
    def init_hand(self)->bool:
        now_hand_lenth=len(self.hand)
        if now_hand_lenth>=5:
            return False
        for i in range(now_hand_lenth,5):
            self.draw()
        return True
        
    def swap_hand_cards(self,hand_index_list:list[int])->bool:
        if self._is_swap_hand:
            return False
        if not hand_index_list:
            self._is_swap_hand=True
            return True
        
        waiting_cards:list[Card]=[]
        for hand_index in hand_index_list:
            try:
                card = self.hand[hand_index]
            except IndexError:
                return False
                # card = None
            if card:
                waiting_cards.append(card)
        for waiting_card in waiting_cards:
            if waiting_card in self.hand:
                self.hand.remove(waiting_card)
        
        self._set_cards_to_waiting_room(waiting_cards)
        self.init_hand()
        self._is_swap_hand=True
        return True
    
    def get_is_swap_hand(self)->bool:
        return self._is_swap_hand
    
    def get_all_stage_status(self)->list:
        if self.playmat:
            return self.playmat.get_all_stage_status()
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    
    def all_stage_rest_stand(self):
        self.playmat.all_stage_rest_stand()
        
    def change_stage_stand(self,stage_index:int,is_stand:bool):
        self.playmat.change_stage_stand(stage_index,is_stand)
        
    def _set_cards_to_waiting_room(self,cards:list[Card]):
        self.playmat.set_cards_to_waiting_room(cards)
    
    def remove_hand(self,index:int)->Card:
        card=None
        if 0 <= index < len(self.hand):
            card=self.hand.pop(index)
        return card
    
    async def set_card_to_clock(
        self,card:Card,
        clock_set_callback:Callable[[int],Awaitable[None]]=None,
        clock_draw_callback:Callable[[bool],Awaitable[None]]=None
    )->bool:
        level_up=self.playmat.set_card_to_clock(card)
        success=False
        if clock_set_callback:
            success=await clock_set_callback(card.card_id)
        if level_up:
            await self._handle_flag_callback("clock")
        if success and clock_draw_callback:
            await clock_draw_callback(level_up)
        return level_up
    
    def check_has_stage_card(self,stage_index:int)->bool:
        if self.playmat:
            return self.playmat.has_stage_card(stage_index)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    
    def read_hand_id(self,hand_index:int)->int:
        if 0<=hand_index<len(self.hand):
            return self.hand[hand_index].card_id
        else:
            raise ValueError("Hand Index Over the Range")
    
    def read_hand_type(self,hand_index:int)->CardType:
        if 0<=hand_index<len(self.hand):
            return self.hand[hand_index].get_card_type()
        else:
            raise ValueError("Hand Index Over the Range")
        
    def pop_hand(self,hand_index:int)->Card:
        if 0<=hand_index<len(self.hand):
            card=self.hand.pop(hand_index)
            return card
        else:
            raise ValueError("Hand Index Over the Range")
        
    def flip_over_deck(self,times:int)->list[Card]:
        cards:list[Card]=[]
        for one_time in times:
            cards.append(self.flip_over_deck_one_card())
        return cards
        
    def flip_over_deck_one_card(self)->Card:
        if self.playmat:
            return self.playmat.flip_over_deck_one_card()
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    
    def set_card_to_stage(self,card:Card,stage_index:int)->bool:
        if self.playmat:
            return self.playmat.set_card_to_stage(card,stage_index)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    
    def set_card_to_resolution(self,card:Card)->bool:
        if self.playmat:
            return self.playmat.set_card_to_resolution(card)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    
    def set_card_to_waiting_room(self,card:Card)->bool:
        if self.playmat:
            return self.playmat.set_card_to_waiting_room(card)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    
    async def start_handle_resolution(self,target:str)->bool:
        if not self.playmat:
            raise ValueError(f"{self.player_id} No Playmat")
        self.playmat.set_next_resolution_target(target)
        for i in range(self.playmat.get_resolution_size()):
            card=self.playmat.resolution_pop(0)
            if not card:
                continue
            flag=await self.playmat.handle_set_card_to_target(card,target)
            if flag:
                await self._handle_flag_callback(target)
                return True
        self.playmat.set_next_resolution_target()
        return False
    
    async def continue_handle_resolution(self,key:str="")->bool:
        if not self.playmat:
            raise ValueError(f"{self.player_id} No Playmat")
        target=self.playmat.get_next_resolution_target()
        if key and target!=key:
            return False
        for i in range(self.playmat.get_resolution_size()):
            card=self.playmat.resolution_pop(0)
            if not card:
                continue
            flag=await self.playmat.handle_set_card_to_target(card,target)
            if flag:
                await self._handle_flag_callback(target)
                return True
        self.playmat.set_next_resolution_target()
        return False
    
    async def _handle_flag_callback(self,name:str):
        callback_name=self.FLAG_CALLBACK_REGISTRY.get(name)
        if callback_name is None:
            return
        callback=getattr(self,callback_name)
        if callback:
            await callback(self.player_id)
    
    async def process_level_up(self,clock_index:int)->bool:
        if not self.playmat:
            raise ValueError(f"{self.player_id} No Playmat")
        if not self.playmat.is_waiting_level_up():
            return False
        level_card=self.playmat.clock_pop(clock_index)
        for i in range(self.playmat.get_clock_size()):
            card=self.playmat.clock_pop(0)
            await self.playmat.handle_set_card_to_target(card,"waiting_room")
        is_defeat=self.playmat.handle_set_card_to_target(level_card,"level")
        if is_defeat:
            await self.Defeat()
        return True
    
    def move_stage_char(self,ori_index:int,tar_index:int):
        if self.playmat:
            return self.playmat.move_stage_char(ori_index,tar_index)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
        
    def check_has_set_cx(self)->bool:
        if self.playmat:
            return self.playmat.check_has_set_cx()
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    
    def set_cx(self,card:Card):
        if self.playmat:
            return self.playmat.set_cx(card)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
        
    def remove_cx(self):
        if self.playmat:
            return self.playmat.remove_cx()
        else:
            raise ValueError(f"{self.player_id} No Playmat")
        
    def get_hand_exceed_limit(self)->int:
        hand_size=len(self.hand)
        if hand_size>setting_ingame.HAND_LIMIT:
            return hand_size-setting_ingame.HAND_LIMIT
        else:
            return 0
        
    def get_stage_card_owner_id(self,stage_index:int)->int:
        if self.playmat:
            return self.playmat.get_stage_card_owner_id(stage_index)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
        
    def get_stage_card_status(self,stage_index:int)->StageStatus:
        if self.playmat:
            return self.playmat.get_stage_card_status(stage_index)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
        
    def set_stage_status(self,stage_index:int,status:StageStatus)->bool:
        if self.playmat:
            return self.playmat.set_stage_status(stage_index,status)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
    
    def get_stage_index_by_status(self,status:StageStatus)->list[int]:
        if self.playmat:
            return self.playmat.get_stage_index_by_status(status)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
        
    def remove_stage_to_waiting_room(self,stage_index:int)->bool:
        if self.playmat:
            return self.playmat.stage_to_waiting_room(stage_index)
        else:
            raise ValueError(f"{self.player_id} No Playmat")
        
    async def Defeat(self):
        if self.on_defeat:
            await self.on_defeat(self.player_id)