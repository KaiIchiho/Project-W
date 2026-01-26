import random
from .base import GameObject
from .card import Card
from typing import Optional,Callable

class Deck(GameObject):
    MAX_CARDS_SIZE=50
    on_deck_empty:Optional[Callable[[],None]]=None
    
    def __init__(self, 
                 object_id,
                 name:str,
                 cards:list[Card]
                 ):
        super().__init__(object_id)
        self.name=name
        if len(cards)!=self.MAX_CARDS_SIZE:
            raise ValueError(
                f"{name} cards size is {len(cards)}, but must contain exactly {self.MAX_CARDS_SIZE} cards"
                )
        self.cards=cards
        
    def shuffle(self):
        random.shuffle(self.cards)
        print(f"{self.name}: shuffle")
        
    def draw(self)->Card:
        print(f"{self.name} Draw")
        if len(self.cards)==0:
            return None
        
        card=self.cards.pop()
        if len(self.cards)==0:
            self.on_deck_empty()
            
        return card