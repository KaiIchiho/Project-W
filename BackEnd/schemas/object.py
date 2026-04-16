from pydantic import BaseModel
from typing import Literal
from schemas.register import register
from pydantic import Field

registry={}

class ObjectBaseData(BaseModel):
    type:str

@register("user",registry)
class UserData(ObjectBaseData):
    # type:Literal["user"]="user"
    type:Literal["user"]=Field(default="user", exclude=True)
    user_id:int=-1
    user_is_player:bool=False

@register("deck",registry)
class DeckData(ObjectBaseData):
    type:Literal["deck"]=Field(default="deck", exclude=True)
    card_num:int=-1
    cards:list[dict]=Field(default_factory=list)

@register("stage",registry)
class StageData(ObjectBaseData):
    type:Literal["stage"]=Field(default="stage", exclude=True)
    card_num:int=-1
    cards:list[dict]=Field(default_factory=lambda:[{"card_id": -1} for _ in range(5)])
    markers:list[list[dict]]=Field(default_factory=lambda:[[] for _ in range(5)])

@register("waiting_room",registry)
class WaitingRoomData(ObjectBaseData):
    type:Literal["waiting_room"]=Field(default="waiting_room", exclude=True)
    card_num:int=-1
    char_card_num:int=-1
    event_card_num:int=-1
    cx_card_num:int=-1
    cards:list[dict]=Field(default_factory=list)

@register("hand",registry)
class HandData(ObjectBaseData):
    type:Literal["hand"]=Field(default="hand", exclude=True)
    card_num:int=-1
    cards:list[dict]=Field(default_factory=list)

@register("clock",registry)
class ClockData(ObjectBaseData):
    type:Literal["clock"]=Field(default="clock", exclude=True)
    card_num:int=-1
    char_card_num:int=-1
    event_card_num:int=-1
    cx_card_num:int=-1
    cards:list[dict]=Field(default_factory=list)
    card_colors:list[str]=Field(default_factory=list)

@register("level",registry)
class LevelData(ObjectBaseData):
    type:Literal["level"]=Field(default="level", exclude=True)
    card_num:int=-1
    char_card_num:int=-1
    event_card_num:int=-1
    cx_card_num:int=-1
    cards:list[dict]=Field(default_factory=list)
    card_colors:list[str]=Field(default_factory=list)

@register("stock",registry)
class StockData(ObjectBaseData):
    type:Literal["stock"]=Field(default="stock", exclude=True)
    card_num:int=-1
    char_card_num:int=-1
    event_card_num:int=-1
    cx_card_num:int=-1
    cards:list[dict]=Field(default_factory=list)
    
    # [{index:1,tirgger:"xxx"},]
    cx_trigger:list[dict]=Field(default_factory=list)

@register("cx",registry)
class CXData(ObjectBaseData):
    type:Literal["cx"]=Field(default="cx", exclude=True)
    card_id:int=-1

@register("memory",registry)
class MemoryData(ObjectBaseData):
    type:Literal["memory"]=Field(default="memory", exclude=True)
    card_num:int=-1
    char_card_num:int=-1
    event_card_num:int=-1
    cx_card_num:int=-1
    cards:list[dict]=Field(default_factory=list)

@register("player",registry)
class PlayerData(ObjectBaseData):
    type:Literal["player"]=Field(default="player", exclude=True)
    user_id:int=-1
    deck:DeckData
    stage:StageData
    waiting_room:WaitingRoomData
    hand:HandData
    clock:ClockData
    level:LevelData
    stock:StockData
    cx:CXData
    memory:MemoryData
 
@register("add_card",registry)
class AddCardData(ObjectBaseData):
     type:Literal["add_card"]=Field(default="add_card", exclude=True)
     card_id:int=-1
     card_img:str=""
    
@register("stage_position",registry)
class StagePositionData(ObjectBaseData):
    type:Literal["stage_position"]=Field(default="stage_position", exclude=True)
    index:int=-1,
    is_empty:bool=False

def build_object_data(type:str,**kwargs)->ObjectBaseData:
    cls=registry.get(type)
    if not cls:
        raise ValueError(f"Unknown object type: {type}")
    return cls(type=type,**kwargs)