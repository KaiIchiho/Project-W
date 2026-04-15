from models.base import GameObject
from models.deck import Deck
from models.card import Card
from typing import Optional,Callable

class Playmat(GameObject):
    on_stage_card_stand_changed:Callable[[int,bool],None]
    
    # deck:Optional[Deck]=None
    
    def __init__(self, 
                 ori_owner_id:int,
                #  deck:Deck=None
                 ):
        super().__init__(ori_owner_id)
        self.deck=None
        self.waiting_room:list[Card]=[]
        
        self.stage:list[Optional[Card]]=[None]*5
        self.markers:list[Optional[list[Card]]]=[None]*5
        self.stage_stand:list[bool]=[True]*5
        
        self.clock:list[Optional[Card]]=[None]*6
        self.level:list[Optional[Card]]=[None]*4
        self.memory:list[Optional[Card]]=[]
        self.climax:Card=None
        self.stock:list[Optional[Card]]=[]
    
    def set_init_deck(self,init_deck:Deck):
        self.deck=init_deck
        self.deck.on_deck_empty=self.reset_deck
    
    def deck_shuffle(self):
        if self.deck:
            self.deck.shuffle()
    
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
    
    def set_card_to_waiting_room(self,card:Card):
        self.waiting_room.append(card)
            
    def set_cards_to_waiting_room(self,cards:list[Card]):
        # self.waiting_room.extend(cards)
        for card in cards:
            self.set_card_to_waiting_room(card)
        
    def set_card_to_clock(self,card:Card)->bool:
        counter=0
        for i in range(len(self.clock)):
            if self.clock[i] is None:
                self.clock[i]=card
                counter+=1
                break
            else:
                counter+=1
        if counter==len(self.clock):
            return True
        else:
            return False
    
    def _level_up(self):
        pass
    
    def has_stage_card(self,stage_index:int)->bool:
        if 0<=stage_index<len(self.stage):
            if self.stage[stage_index]:
                return True
            else:
                return False
        else:
            raise ValueError("Stage Index Over the Range")
        
    def set_card_to_stage(self,card:Card,stage_index:int)->bool:
        if not card:
            return False
        if 0<=stage_index<len(self.stage):
            stage=self.stage[stage_index]
            self.stage[stage_index]=card
            if stage:
                self.set_card_to_waiting_room(stage)
            return True
        else:
            raise ValueError("Stage Index Over the Range")