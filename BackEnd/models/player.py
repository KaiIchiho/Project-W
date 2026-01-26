from .base import GameObject
from .card import Card
from .playmat import Playmat
from typing import Optional

class Player(GameObject):
    def __init__(self,
                 object_id,
                 player_id:str,
                 name:str,
                 playmat:Playmat
                 ):
        super().__init__(object_id)
        self.player_id=player_id
        self.name=name
        self.playmat=playmat
        self.hand:list[Optional[Card]]=[None]*7
        
    def draw(self):
        print(f"{self.name} Draw")
        for i in range(len(self.hand)):
            if self.hand[i] is None:
                self.hand[i]=self.playmat.deck.draw()
        
    def play_command(self):
        print(f"{self.name} Play Command")
        
    def init_hand(self):
        self.__organize_hand()
        for i in range(5):
            if self.hand[i] is None:
                self.draw()
                
    def __organize_hand(self):
        cards=[card for card in self.hand if card is not None]
        nones=[None]*(len(self.hand)-len(cards))
        self.hand=cards+nones
        
    def manage_hand(self,selected_card:list[Card]):
        if not selected_card:
            return
        for i in len(self.hand):
            if self.hand[i] in selected_card:
                self.playmat.set_card_to_memory(self.hand[i])
                self.hand[i]=None
        self.int_hand()
    
    def all_stage_stand(self):
        self.playmat.all_stage_stand()
        
    def change_stage_stand(self,stage_index:int,is_stand:bool):
        self.playmat.change_stage_stand(stage_index,is_stand)