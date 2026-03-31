from db import crud
from config.setting_database import DECK_TABLE,DECK_CARDS_TABLE

# Deck
def read_all_deck()->list[dict]:
    return crud.read_all_data_by_table(DECK_CARDS_TABLE)

def test_read_all_deck(deck_id:int):
    deck_cards=read_cards_info_by_deck_id(deck_id)
    result=process_deck_cards_info(deck_cards)
    for data in result:
        print(data)

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