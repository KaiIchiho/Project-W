import random
from models.base import GameObject
from models.card import Card
from typing import Optional,Callable
from db import deck_repo

class Deck(GameObject):
    MAX_CARDS_SIZE=50
    on_deck_empty:Optional[Callable[[],None]]=None
    
    def __init__(self, 
                 ori_owner_id:int,
                #  deck_id:int
                #  cards:list[Card]
                 ):
        super().__init__(ori_owner_id)
        self._deck_id=-1
        self._deck_name=""
        self.cards:list[Card]=None
        
    def init_deck_by_deck_id(self,deck_id:int)->bool:
        print(f"Log: init_deck_by_deck_id, ID: {self._deck_id}")
        self._deck_id=deck_id
        card_info_list=deck_repo.read_cards_info_by_deck_id(self._deck_id)
        if not card_info_list:
            return False
        card_id_list=deck_repo.process_deck_cards_info(card_info_list)
        print(f"Log:card_id_list, {card_id_list}")
        if not card_id_list:
            return False
        return self.init_deck_by_card_id(card_id_list)
        
    def init_deck_by_card_id(self,card_id_list:list[int])->bool:
        if len(card_id_list)!=self.MAX_CARDS_SIZE:
            return False
        card_list:list[Card]=[]
        for card_id in card_id_list:
            card=Card(self.ori_owner_id,card_id)
            card_list.append(card)
        self.cards=card_list
        return True
    
    def shuffle(self):
        random.shuffle(self.cards)
        print(f"{self.ori_owner_id}: shuffle")
        
    def draw(self)->Card:
        print(f"{self.ori_owner_id} Draw")
        if len(self.cards)==0:
            return None
        
        card=self.cards.pop()
        if len(self.cards)==0:
            self.on_deck_empty()
            
        return card