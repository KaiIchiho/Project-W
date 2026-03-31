from db import crud
from config.setting_database import CARD_TABLE

# Card
def read_all_card():
    return crud.read_all_data_by_table(CARD_TABLE)

def test_read_all_card():
    card_list=read_all_card()
    for card in card_list:
        print(card)

def read_card_info(card_id:int)->list[dict]:
    result=crud.read_data_by_id(CARD_TABLE,card_id)
    if result:
        print(f"ID: {card_id}, Card Info: ",result)
    return result