from models.base import GameObject
from models.deck import Deck
from models.card import Card
from typing import Optional,Callable

class Playmat(GameObject):
    on_stage_card_stand_changed:Callable[[int,bool],None]
    
    deck:Optional[Deck]=None
    
    def __init__(self, 
                 ori_owner_id:int,
                 deck:Deck=None
                 ):
        super().__init__(ori_owner_id)
        self.deck=deck
        self.waiting_room:list[Card]=[]
        
        self.stage:list[Optional[Card]]=[None]*5
        self.stage_stand:list[bool]=[True]*5
        
        self.clock:list[Optional[Card]]=[None]*6
        self.level:list[Optional[Card]]=[None]*4
        self.memory:list[Optional[Card]]=[]
        self.climax:Card=None
        self.stock:list[Optional[Card]]=[]
        
        self.deck.on_deck_empty=self.reset_deck
            
    def reset_deck(self):
        if self.deck is None:
            return
        
    def set_card_to_memory(self,card:Card):
        self.climax=card
        
    def all_stage_stand(self):
        for i in range(len(self.stage_stand)):
            self.change_stage_stand(i,True)
        
    def change_stage_stand(self,stage_index:int,is_stand:bool):
        if not 0<=stage_index<5:
            return
        if self.stage_stand[stage_index]!=is_stand:
            self.stage_stand[stage_index]=is_stand
            self.on_stage_card_stand_changed(stage_index,is_stand)