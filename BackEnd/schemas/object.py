from pydantic import BaseModel
from typing import Literal
from schemas.register import register

registry={}

class ObjectBaseData(BaseModel):
    type:str

@register("user",registry)
class UserData(ObjectBaseData):
    type:Literal["user"]
    user_id:int
    user_is_player:bool

@register("memory",registry)
class MemoryData(ObjectBaseData):
    type:Literal["memory"]
    card_num:int
    card_id_list:list[int]

@register("cx",registry)
class CXData(ObjectBaseData):
    type:Literal["cx"]
    card_id:int

@register("stock",registry)
class StockData(ObjectBaseData):
    type:Literal["stock"]
    card_num:int
    card_id_list:list[int]

@register("level",registry)
class LevelData(ObjectBaseData):
    type:Literal["level"]
    card_num:int
    card_id_list:list[int]

@register("clock",registry)
class ClockData(ObjectBaseData):
    type:Literal["clock"]
    card_num:int
    card_id_list:list[int]

@register("hand",registry)
class HandData(ObjectBaseData):
    type:Literal["hand"]
    card_num:int
    card_id_list:list[int]

@register("waiting_room",registry)
class WaitingRoomData(ObjectBaseData):
    type:Literal["waiting_room"]
    card_num:int
    card_id_list:list[int]

@register("deck",registry)
class DeckData(ObjectBaseData):
    type:Literal["deck"]
    card_num:int
    card_id_list:list[int]

@register("player",registry)
class PlayerData(ObjectBaseData):
    type:Literal["player"]
    user_id:int
    deck:DeckData
    waiting_room:WaitingRoomData
    hand:HandData
    clock:ClockData
    level:LevelData
    stock:StockData
    cx:CXData
    memory:MemoryData
    
    
def build_object_data(type:str,**kwargs)->ObjectBaseData:
    cls=register.get(type)
    if not cls:
        raise ValueError(f"Unknown object type: {type}")
    return cls(type=type,**kwargs)