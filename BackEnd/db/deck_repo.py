from db import crud
from config.setting_database import DECK_TABLE,DECK_CARDS_TABLE

# Deck
def read_all_deck()->list[dict]:
    return crud.read_all_data_by_table(DECK_TABLE)

def read_deck_by_id(deck_id:int)->dict:
    return crud.read_data_by_id(DECK_TABLE,deck_id)

def read_deck_name_by_id(deck_id:int):
    deck=crud.read_data_by_id(DECK_TABLE,deck_id)
    if not deck:
        return None
    name=deck.get("name")
    return name

def read_cards_info_by_deck_id(deck_id:int):
    result=crud.read_data_by_value(DECK_CARDS_TABLE,"deck_id",deck_id)
    return result

def process_deck_cards_info(deck_cards_info:list[dict]):
    card_list=[]
    for deck_card in deck_cards_info:
        card_id=deck_card.get("card_id")
        quantity=deck_card.get("quantity")
        if card_id is None or quantity is None:
            continue
        card_list.extend([card_id]*quantity)
    return card_list
