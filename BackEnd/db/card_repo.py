from db import crud
from config.setting_database import CARD_TABLE

allowed_fields={
    "card_img":"card_img",
    "card_color":"card_color",
    "card_trigger":"card_trigger",
    "card_power":"card_power",
    "card_level":"card_level",
    "card_cost":"card_cost",
    "card_name":"card_name",
    "card_side":"card_side",
    "card_type":"card_type",
    "card_soul":"card_soul",
    "card_trait1":"card_trait1",
    "card_trait2":"card_trait2",
    "card_trait3":"card_trait3",
    "card_effect_text":"card_effect_text",
    "card_effect_data":"card_effect_data",
    "card_is_wildcard":"card_is_wildcard",
    "card_has_counter_icon":"card_has_counter_icon",
    "card_has_clock_icon":"card_has_clock_icon",
    "card_has_cx_combo":"card_has_cx_combo"
}

# Card
def read_all_card():
    return crud.read_all_data_by_table(CARD_TABLE)

# def test_read_all_card():
#     card_list=read_all_card()
#     for card in card_list:
#         print(card)

def read_card_info(card_id:int)->list[dict]:
    result=crud.read_data_by_id(CARD_TABLE,card_id)
    if result:
        print(f"ID: {card_id}, Card Info: ",result)
    return result

def read_card_field(card_id:int,field:str):
    if field not in allowed_fields:
        raise ValueError("invalid card field")
    return crud.read_field_value(CARD_TABLE,card_id,field)

def read_card_field_list(card_id:int,field_list:list[str])->dict:
    field_value={}
    for field in field_list:
        value=read_card_field(card_id,field)
        field_value[field]=value
    print("Log: read_card_field_list")
    print(field_value)