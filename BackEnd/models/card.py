from models.base import GameObject
from db import card_repo
from core.card_type import CardType

class Card(GameObject):
    def __init__(self, 
                 ori_owner_id:int,
                 card_id:int):
        super().__init__(ori_owner_id)
        self.owner_id=ori_owner_id
        
        self.card_id=card_id
        self.image_filename:str=""
        self.color:str=""
        self.trigger_type:str=""
        self.power:int=-1
        self.level:int=-1
        self.cost:int=-1
        self.name:str=""
        self.side:str=""
        self.type:str=""
        self.soul:int=-1
        self.trait1:str=""
        self.trait2:str=""
        self.trait3:str=""
        self.effect_text:str=""
        self.effect_data:dict={}
        self.is_wildcard:bool=False
        self.has_counter_icon:bool=False
        self.has_clock_icon:bool=False
        self.has_cx_combo:bool=False
        
        self.init_info()
        self.type_enum=CardType(self.type)
        self.triggers:list[str]=self.process_triggers()
        
    def init_info(self):
        key_list=[]
        for key in card_repo.allowed_fields:
            key_list.append(key)
        key_value=card_repo.read_card_field_list(self.card_id,key_list)
        for key,value in key_value.items():
            self._set_current_info(key,value)
    
    def _set_current_info(self,info_name:str,value):
        value_name=card_repo.allowed_fields.get(info_name)
        print(f"Log: value_name: {value_name}, info_name: {info_name}")
        print(f"Log: value: {value}")
        if value_name and hasattr(self,value_name):
            setattr(self,value_name,value)
            print(f"Log: Card Id: {self.card_id}")
            print(f"{value_name} : {value}")
            
    def get_current_info(self,info_name:str):
        if info_name!="card_id":
            value_name=card_repo.allowed_fields.get(info_name)
        else:
            value_name=info_name
        if not value_name:
            return None
        value=getattr(self,value_name,None)
        return value
    
    def get_current_info_by_list(self,info_name_list:list[str])->dict:
        info_dict={}
        for info_name in info_name_list:
            value=self.get_current_info(info_name)
            # if value is not None:
            info_dict[info_name]=value
            
        return info_dict
    
    def process_triggers(self)->list[str]:
        triggers=self.trigger_type.split(",")
        return triggers
    
    def get_triggers(self)->list[str]:
        return self.triggers