from pydantic import BaseModel,Field

class ClockPhaseClockHandCard(BaseModel):
    hand_index:int=-1

class MainPhaseEventPlayUserCard(BaseModel):
    hand_index:int=-1