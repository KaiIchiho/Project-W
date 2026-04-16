from models.base import GameObject
from db import card_repo

class Card(GameObject):
    card_id:int
    image_filename:str
    color:str
    trigger_type:str
    power:int
    level:int
    cost:int
    name:str
    side:str
    type:str
    soul:int
    trait1:str
    trait2:str
    trait3:str
    effect_text:str
    effect_data:dict
    is_wildcard:bool
    has_counter_icon:bool
    has_clock_icon:bool
    has_cx_combo:bool
    def __init__(self, 
                 ori_owner_id:int,
                 card_id:int):
        super().__init__(ori_owner_id)
        self.card_id=card_id
        self.init_info()
        
    def init_info(self):
        key_list=[]
        for key in card_repo.allowed_fields:
            key_list.append(key)
        key_value=card_repo.read_card_field_list(self.card_id,key_list)
        for key,value in key_value.items():
            self._set_current_info(key,value)
    
    def _set_current_info(self,info_name:str,value):
        value_name=card_repo.allowed_fields.get(info_name)
        if value_name and hasattr(self,value_name):
            setattr(self,value_name,value)
            
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