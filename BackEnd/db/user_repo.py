from db import crud
from config.setting_database import USER_TABLE

def read_all_users()->list[dict]:
    return crud.read_all_data_by_table(USER_TABLE)

def check_is_user_exist(user_id)->bool:
    return crud.check_is_id_exist_by_table(USER_TABLE,user_id)

# None Or Intager
def check_name_and_pw(user_name,password)->int:
    result=None
    user_list=read_all_users()
    if not user_list or not len(user_list):
        return result
    for user_data in user_list:
        print(
            f"user id: {user_data.get('id')}, name: {user_data.get('name')}, password: {user_data.get('password')}")
        
        name=user_data.get("name")
        pw=user_data.get("password")
        if name==user_name and pw==password:
            result=user_data.get("id")
            break
    
    return result