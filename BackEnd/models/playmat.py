from models.base import GameObject
from models.deck import Deck
from models.card import Card
from typing import Optional,Callable
from config import setting_ingame
from enum import Enum

class StageStatus(str,Enum):
    STAND="stand"
    REST="rest"
    REVERSE="reverse"

class Playmat(GameObject):
    on_stage_card_stand_changed:Callable[[int,StageStatus],None]=None
    
    # deck:Optional[Deck]=None
    
    def __init__(self, 
                 ori_owner_id:int,
                #  deck:Deck=None
                 ):
        super().__init__(ori_owner_id)
        self.deck:Deck=None
        self.waiting_room:list[Card]=[]
        
        self.stage:list[Optional[Card]]=\
            [None]*setting_ingame.STAGE_SIZE
        self.markers:list[list[Card]]=\
            [[] for _ in range(setting_ingame.STAGE_SIZE)]
        self.stage_status:list[StageStatus]=\
            [None]*setting_ingame.STAGE_SIZE
        # self.stage_stand:list[bool]=[True]*5
        
        # self.clock:list[Optional[Card]]=[None]*6
        self.clock:list[Card]=[]
        # self.level:list[Optional[Card]]=[None]*4
        self.level:list[Card]=[]
        self.memory:list[Card]=[]
        self.climax:Card=None
        self.stock:list[Card]=[]
        self.resolution:list[Card]=[]
    
    def set_init_deck(self,init_deck:Deck):
        self.deck=init_deck
        self.deck.on_deck_empty=self.reset_deck
    
    def get_deck_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        if self.deck:
            return self.deck.get_cards_info_by_list(card_info_list)
        else:
            raise ValueError("Deck Invailed")
    def get_stage_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        cards_info=[]
        for card in self.stage:
            if card is None:
                cards_info.append({})
                continue
            card_info=card.get_current_info_by_list(card_info_list)
            cards_info.append(card_info)
        return cards_info
    def get_marker_cards_info_by_list(self,card_info_list:list[str])->list[list[dict]]:
        marker_info=[]
        for marker in self.markers:
            cards_info=[]
            for card in marker:
                if card is None:
                    continue
                card_info=card.get_current_info_by_list(card_info_list)
                cards_info.append(card_info)
            marker_info.append(cards_info)
        return marker_info
    def get_waiting_room_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        cards_info=[]
        for card in self.waiting_room:
            if card is None:
                continue
            card_info=card.get_current_info_by_list(card_info_list)
            cards_info.append(card_info)
        return cards_info
    def get_clock_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        cards_info=[]
        for card in self.clock:
            if card is None:
                continue
            card_info=card.get_current_info_by_list(card_info_list)
            cards_info.append(card_info)
        return cards_info
    def get_level_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        cards_info=[]
        for card in self.level:
            if card is None:
                continue
            card_info=card.get_current_info_by_list(card_info_list)
            cards_info.append(card_info)
        return cards_info
    def get_stock_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        cards_info=[]
        for card in self.stock:
            if card is None:
                continue
            card_info=card.get_current_info_by_list(card_info_list)
            cards_info.append(card_info)
        return cards_info
    def get_climax_id(self)->int:
        if self.climax:
            return self.climax.card_id
        else:
            return -1
    def get_climax_card_info_by_list(self,card_info_list:list[str])->dict:
        if self.climax:
            return self.climax.get_current_info_by_list(card_info_list)
        else:
            return {}
    def get_memory_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        cards_info=[]
        for card in self.memory:
            if card is None:
                continue
            card_info=card.get_current_info_by_list(card_info_list)
            cards_info.append(card_info)
        return cards_info
    def get_resolution_cards_info_by_list(self,card_info_list:list[str])->list[dict]:
        cards_info=[]
        for card in self.resolution:
            if card is None:
                continue
            card_info=card.get_current_info_by_list(card_info_list)
            cards_info.append(card_info)
        return cards_info
    
    def deck_shuffle(self):
        if self.deck:
            self.deck.shuffle()
    
    def reset_deck(self):
        if self.deck is None:
            return
        
    def set_card_to_memory(self,card:Card):
        self.climax=card
    
    def get_all_stage_status(self)->list:
        status_list=[]
        for status in self.stage_status:
            status_str=status.value if status else ""
            status_list.append(status_str)
        return status_list
    
    def all_stage_rest_stand(self):
        for i in range(len(self.stage_status)):
            self.change_stage_status(i,StageStatus.STAND,StageStatus.REST)
        
    def change_stage_status(self,stage_index:int,status:StageStatus,condition_status:StageStatus=None):
        if not 0<=stage_index<5:
            return
        if condition_status and self.stage_status[stage_index]!=condition_status:
            return
        self.stage_status[stage_index]=status
        if self.on_stage_card_stand_changed:
            self.on_stage_card_stand_changed(stage_index,status)
    
    def set_card_to_waiting_room(self,card:Card)->bool:
        if not card:
            return False
        card.init_info()
        self.waiting_room.append(card)
        return True
    
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
        if counter==setting_ingame.CLOCK_LIMIT:
            return True
        else:
            return False
    
    def set_card_to_stock(self,card:Card)->bool:
        if not card:
            return False
        card.init_info()
        self.stock.append(card)
        return True
    
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
            self.stage_status[stage_index]=status
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
            self.set_card_to_waiting_room(self.resolution.pop(0))
    def resolution_to_stock(self):
        num=len(self.resolution)
        for i in range(num):
            print("Log: 1 Resolution Card Switch To Waiting Room")
            self.set_card_to_stock(self.resolution.pop(0))
    def resolution_to_clock(self):
        num=len(self.resolution)
        for i in range(num):
            print("Log: 1 Resolution Card Switch To Waiting Room")
            self.set_card_to_clock(self.resolution.pop(0))
            
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
    
    def check_has_set_cx(self):
        if self.climax:
            return True
        else:
            return False
    
    def remove_cx(self):
        if self.climax:
            card=self.climax
            self.climax=None
            self.set_card_to_waiting_room(card)
        
    def set_cx(self,card:Card):
        self.remove_cx()
        self.climax=card
        
    def flip_over_deck_one_card(self)->Card:
        return self.deck.draw()
    
    def get_stage_card_owner_id(self,stage_index:int)->int:
        if 0<=stage_index<len(self.stage):
            if self.stage[stage_index] is None:
                return -1
            return self.stage[stage_index].owner_id
        else:
            return -1
        
    def get_stage_card_status(self,stage_index:int)->StageStatus:
        if 0<=stage_index<len(self.stage_status):
            return self.stage_status[stage_index]
        else:
            return None
        
    def set_stage_status(self,stage_index:int,status:StageStatus)->bool:
        if 0<=stage_index<len(self.stage_status):
            if self.stage_status[stage_index] is None:
                return False
            else:
                self.stage_status[stage_index]=status
                return True
        else:
            return False
        
    def get_stage_index_by_status(self,status:StageStatus)->list[int]:
        index_list=[]
        for i in range(len(self.stage_status)):
            if self.stage_status[i] is None:
                continue
            if self.stage_status[i]==status:
                index_list.append(i)
        return index_list
    
    def stage_to_waiting_room(self,stage_index:int)->bool:
        if 0<=stage_index<len(self.stage_status):
            if self.stage[stage_index]:
                card=self.stage[stage_index]
                self.stage[stage_index]=None
                self.stage_status[stage_index]=None
                self.set_card_to_waiting_room(card)
                return True
            else:
                return False
        else:
            return False