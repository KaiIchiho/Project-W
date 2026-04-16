from models.base import GameObject
from models.card import Card
from models.deck import Deck
from models.playmat import Playmat
from typing import Optional

class Player(GameObject):    
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
    
    def all_stage_stand(self):
        self.playmat.all_stage_stand()
        
    def change_stage_stand(self,stage_index:int,is_stand:bool):
        self.playmat.change_stage_stand(stage_index,is_stand)
        
    def _set_cards_to_waiting_room(self,cards:list[Card]):
        self.playmat.set_cards_to_waiting_room(cards)
    
    def remove_hand(self,index:int)->Card:
        card=None
        if 0 <= index < len(self.hand):
            card=self.hand.pop(index)
        return card
    
    def set_card_to_clock(self,card:Card)->bool:
        return self.playmat.set_card_to_clock(card)
    
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
        
    def pop_hand(self,hand_index:int)->Card:
        if 0<=hand_index<len(self.hand):
            card=self.hand.pop(hand_index)
            return card
        else:
            raise ValueError("Hand Index Over the Range")
        
    def set_card_to_stage(self,card:Card,stage_index:int)->bool:
        if self.playmat:
            return self.playmat.set_card_to_stage(card,stage_index)
        else:
            raise ValueError(f"{self.player_id} No Playmat")