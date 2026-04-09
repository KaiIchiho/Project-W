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
        #self.hand:list[Optional[Card]]=[None]*7
        self.hand:list[Card]=[]
    
    def set_deck_id(self,deck_id:int)->bool:
        self._deck_id=deck_id
        return True
    
    def check_has_deck(self)->bool:
        if self._deck_id==-1:
            return False
        else:
            return True
    
    def init_playmat(self):
        self.playmat=Playmat(self.ori_owner_id)
        deck=Deck(self.ori_owner_id)
        if not deck.init_deck_by_deck_id(self._deck_id):
            return False
        self.playmat.set_init_deck(deck)
        self.playmat.deck_shuffle()
        return True
    
    def draw(self):
        print(f"{self.name} Draw")
        #for i in range(len(self.hand)):
        #    if self.hand[i] is None:
        #        self.hand[i]=self.playmat.deck.draw()
        self.hand.append(self.playmat.deck.draw())
        
    #def play_command(self):
    #    print(f"{self.name} Play Command")
        
    def init_hand(self)->bool:
        now_hand_lenth=len(self.hand)
        if now_hand_lenth>=5:
            return False
        for i in range(now_hand_lenth,5):
            self.draw()
        return True
                
    #def __organize_hand(self):
    #    cards=[card for card in self.hand if card is not None]
    #    nones=[None]*(len(self.hand)-len(cards))
    #    self.hand=cards+nones
        
    def swap_hand_cards(self,hand_index_list:list[int])->bool:
        if not hand_index_list:
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
        return self.init_hand()
        
        # for i in len(self.hand):
        #     if self.hand[i] in selected_card:
        #         self.playmat.set_card_to_memory(self.hand[i])
        #         self.hand[i]=None
        # self.int_hand()
    
    def all_stage_stand(self):
        self.playmat.all_stage_stand()
        
    def change_stage_stand(self,stage_index:int,is_stand:bool):
        self.playmat.change_stage_stand(stage_index,is_stand)
        
    def _set_cards_to_waiting_room(self,cards:list[Card]):
        self.playmat.set_cards_to_waiting_room(cards)