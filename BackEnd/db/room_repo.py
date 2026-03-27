from db import crud
from config.setting_database import ROOM_TABLE

def read_all_rooms()->list[dict]:
    return crud.read_all_data_by_table(ROOM_TABLE)

def check_is_room_exist(room_id)->bool:
    return crud.check_is_id_exist_by_table(ROOM_TABLE,room_id)

def insert_room_data(room_id:int,room_name:str)->bool:
    sql=f"INSERT INTO {ROOM_TABLE} (id, name) VALUES (?, ?)"
    params=(room_id,room_name)
    return crud.insert_data(sql,params) 
    