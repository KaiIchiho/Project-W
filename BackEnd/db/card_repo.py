from db import crud
from config.setting_database import CARD_TABLE
from core.card_type import CardType

allowed_fields={
    "card_img":"image_filename",
    "card_color":"color",
    "card_trigger":"trigger_type",
    "card_power":"power",
    "card_level":"level",
    "card_cost":"cost",
    "card_name":"name",
    "card_side":"side",
    "card_type":"type",
    "card_soul":"soul",
    "card_trait1":"trait1",
    "card_trait2":"trait2",
    "card_trait3":"trait3",
    "card_effect_text":"effect_text",
    "card_effect_data":"effect_data",
    "card_is_wildcard":"is_wildcard",
    "card_has_counter_icon":"has_counter_icon",
    "card_has_clock_icon":"has_clock_icon",
    "card_has_cx_combo":"has_cx_combo"
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
    field_name=allowed_fields.get(field)
    result=None
    result_list=crud.read_field_value(CARD_TABLE,card_id,field_name)
    if result_list:
        result_dict=result_list[0]
        result=result_dict.get(field_name)
    return result

def read_card_field_list(card_id:int,field_list:list[str])->dict:
    field_value={}
    for field in field_list:
        value=read_card_field(card_id,field)
        field_value[field]=value
    # print("Log: read_card_field_list")
    # print(field_value)
    return field_value

def read_card_type(card_id:int)->CardType:
    type=read_card_field(card_id,"card_type")
    try:
        return CardType(type)
    except ValueError:
        return None