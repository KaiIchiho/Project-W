from models.base import GameObject

class Card(GameObject):
    def __init__(self, 
                 ori_owner_id:int,
                 card_id:int):
        super().__init__(ori_owner_id)
        self.card_id=card_id