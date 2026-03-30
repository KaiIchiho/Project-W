from db import crud
from config.setting_database import DECK_TABLE

def read_all_deck()->list[dict]:
    return crud.read_all_data_by_table(DECK_TABLE)

def test_read_all_deck():
    deck_list=read_all_deck()
    for deck in deck_list:
        print(deck)