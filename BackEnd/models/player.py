from models.base import GameObject
from models.card import Card
from models.deck import Deck
from models.playmat import Playmat
from core.card_type import CardType
from config import setting_ingame
from models.playmat import StageStatus
from typing import Callable,Awaitable
from db import deck_repo

class Player(GameObject):
    handle_level_up:Callable[[int],Awaitable[None]]=None
    on_defeat:Callable[[int],Awaitable[None]]=None
    on_refresh:Callable[[int],Awaitable[None]]=None
    
    FLAG_CALLBACK_REGISTRY:dict={
        "clock":"handle_level_up",
        "level":"on_defeat"
    }
    
    def __init__(self,
                 player_id:int,
                 name:str,
                 playmat:Playmat=None
                 ):
        super().__init__(player_id)
        self._deck_id:int=-1
        self._deck_name:str=""
        self.player_id=player_id
        self.name=name
        self.playmat=playmat
        self.hand:list[Card]=[]
        
        self._is_swap_hand:bool=False
    
    def set_deck_id(self,deck_id:int)->bool:
        self._deck_id=deck_id
        self._deck_name=deck_repo.read_deck_name_by_id(deck_id)
        return True
    def get_deck_id(self)->int:
        return self._deck_id
    def get_deck_name(self)->str:
        return self._deck_name
    
    def init_playmat(self)->bool:
        self.playmat=Playmat(self.ori_owner_id)
        deck=Deck(self.ori_owner_id)
        deck.on_deck_empty=self.on_deck_empty
        if not deck.init_deck_by_deck_id(self._deck_id,self._deck_name):
            return False
        self.playmat.set_init_deck(deck)
        # self.playmat.deck_shuffle()
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
        
    def deck_shuffle(self)->bool:
        if self.playmat:
            self.playmat.deck_shuffle()
            return True
        else:
            return False
    
    # デッキからカードを引いて手札に加える
    async def draw(self)->int:
        print(f"{self.name} Draw")
        draw_card=await self.playmat.deck.draw()
        self.hand.append(draw_card)
        return draw_card.card_id
        
    async def on_deck_empty(self):
        print("Deck is Empty")
        result=self.refresh()
        if not result:
            print(f"{self.player_id} refresh failed")
            return
        await self.rule_damage(setting_ingame.REFRESH_RULE_DAMAGE)
        if self.on_refresh:
            await self.on_refresh(self.player_id)
    
    def refresh(self)->bool:
        if not self.playmat:
            raise ValueError(f"{self.player_id} No Playmat")
        return self.playmat.refresh()
    
    async def rule_damage(self,damage:int):
        for _ in range(damage):
            card=await self.flip_over_deck_one_card()
            await self.set_card_to_clock(card)
    
    async def init_hand(self)->bool:
        now_hand_lenth=len(self.hand)
        if now_hand_lenth>=5:
            return False
        for i in range(now_hand_lenth,5):
            await self.draw()
        return True
    
    # 選択した手札を控え室に置いて、残りの手札を引き直す
    async def swap_hand_cards(self,hand_index_list:list[int])->bool:
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
        await self.init_hand()
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
    
    # カードをクロック置き場に置く
    # レベルアップしたらレベルアップの処理も行う
    # レベルアップかどうかを返す
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
        
    async def flip_over_deck(self,times:int)->list[Card]:
        cards:list[Card]=[]
        for one_time in times:
            cards.append(await self.flip_over_deck_one_card())
        return cards
    
    # デッキの一番上のカードをめくる
    async def flip_over_deck_one_card(self)->Card:
        if self.playmat:
            return await self.playmat.flip_over_deck_one_card()
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
        return await self._handle_resolution(target)
    
    async def continue_handle_resolution(self,key:str="")->bool:
        if not self.playmat:
            raise ValueError(f"{self.player_id} No Playmat")
        target=self.playmat.get_next_resolution_target()
        if key and target!=key:
            return False
        return await self._handle_resolution(target)
        
    async def _handle_resolution(self,target:str)->bool:
        for i in range(self.playmat.get_resolution_size()):
            card=self.playmat.resolution_pop(0)
            if not card:
                continue
            flag=self.playmat.handle_set_card_to_target(card,target)
            if flag:
                await self._handle_flag_callback(target)
                return True
        self.playmat.set_next_resolution_target()
        return False
    
    # 置き場にカードのセットによりフラグが立った時、
    # 対応するplayer_idをパラメータにするコールバックを呼び出す
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
            self.playmat.handle_set_card_to_target(card,"waiting_room")
        is_defeat=self.playmat.handle_set_card_to_target(level_card,"level")
        if is_defeat:
            # await self._on_defeat()
            await self._handle_flag_callback("level")
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
    
    # ゲーム進行中のプレイヤーのデッキの情報を取得する
    def get_deck_info(self):
        if self.playmat:
            return self.playmat.get_deck_info()
        else:
            raise ValueError(f"{self.player_id} No Playmat")