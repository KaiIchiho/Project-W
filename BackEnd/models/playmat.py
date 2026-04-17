from models.base import GameObject
from models.deck import Deck
from models.card import Card
from typing import Optional,Callable
from enum import Enum

class StageStatus(str,Enum):
    STAND="stand"
    REST="rest"
    REVERSE="reverse"

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
        self.markers:list[list[Card]]=[[] for _ in range(5)]
        self.stage_status:list[StageStatus]=[None]*5
        self.stage_stand:list[bool]=[True]*5
        
        self.clock:list[Optional[Card]]=[None]*6
        self.level:list[Optional[Card]]=[None]*4
        self.memory:list[Card]=[]
        self.climax:Card=None
        self.stock:list[Card]=[]
        self.resolution:list[Card]=[]
    
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
        
    def set_card_to_stage(self,card:Card,stage_index:int,status:StageStatus=StageStatus.STAND)->bool:
        if not card:
            return False
        if 0<=stage_index<len(self.stage):
            stage=self.stage[stage_index]
            self.stage[stage_index]=card
            self.stage_stand[stage_index]=status
            if stage:
                self.set_card_to_waiting_room(stage)
            return True
        else:
            raise ValueError("Stage Index Over the Range")
        
    def set_card_to_resolution(self,card:Card)->bool:
        if not card:
            return False
        self.resolution.append(card)
        return True
    
    def resolution_to_waiting_room(self):
        num=len(self.resolution)
        for i in range(num):
            print("Log: 1 Resolution Card Switch To Waiting Room")
            self.waiting_room.append(self.resolution.pop(0))
            
    def move_stage_char(self,ori_index:int,tar_index:int):
        result=False
        tar_card_id=None
        ori_card_id=None
        ori_origin_status=""
        ori_card_status=""
        tar_origin_status=""
        tar_card_status=""
        if 0<=ori_index<len(self.stage) and 0<=tar_index<len(self.stage):
            card=self.stage[ori_index]
            tar_card_id=self.stage[tar_index].card_id if self.stage[tar_index] else None
            ori_origin_status=self.stage_status[ori_index].value
            tar_origin_status=self.stage_status[tar_index].value if self.stage_status[tar_index] else None
            if not card:
                return result,ori_card_id,tar_card_id,ori_origin_status,tar_origin_status,ori_card_status,tar_card_status
            ori_card_id=card.card_id
            
            self.stage[ori_index],self.stage[tar_index]=\
                self.stage[tar_index],self.stage[ori_index]
            self.stage_status[ori_index],self.stage_status[tar_index]=\
                self.stage_status[tar_index],self.stage_status[ori_index]
            
            ori_card_status=self.stage_status[ori_index].value if self.stage_status[ori_index] else None
            tar_card_status=self.stage_status[tar_index].value
            result=True
            
        return result,ori_card_id,tar_card_id,ori_origin_status,tar_origin_status,ori_card_status,tar_card_status