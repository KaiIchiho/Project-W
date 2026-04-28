from pydantic import BaseModel,Field

class ClockPhaseClockHandCard(BaseModel):
    hand_index:int=-1

class MainPhaseEventPlayUserCard(BaseModel):
    hand_index:int=-1
    
class MainPhaseCharMoveStagePos(BaseModel):
    index:int=-1
    
# class AttackPhaseEncoreOrder(BaseModel):
#     card_id:int=-1