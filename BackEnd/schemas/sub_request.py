from pydantic import BaseModel,Field

class MainPhaseEventPlayUserCard(BaseModel):
    hand_index:int=-1