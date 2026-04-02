from services import game_flow
from services import room
from schemas.room import EnterRoomRequest,ExitRoomRequest
from schemas.game_flow import StandbyRequest,StandbyResponse

def parse_model(data: dict, model_cls):
    try:
        return model_cls.model_validate(data)
    except Exception as e:
        print("Model Parse Failed:", e)
        return None
    
async def handle_standby(data:dict,user_id:int):
    req=parse_model(data,StandbyRequest)
    if not req:
        raise ValueError("StandbyRequest Parse Failed")
    # result=game_flow.standby(user_id)
    # success=False
    # log=""
    
    # res=StandbyResponse(
    #     event=data.get("event"),
    #     success=success,
    #     log=log)
    res=game_flow.standby(user_id,data.get("event"))
    room_id=room.check_user_room(user_id)
    if game_flow.ws_send_data_to_room_handler:
        await game_flow.ws_send_data_to_room_handler(room_id,res)
    
async def handle_enter_room(data:dict,user_id:int):
    print("handle_enter_room")
    req=parse_model(data,EnterRoomRequest)
    if not req:
        raise ValueError("EnterRoomRequest Parse Failed")
    res=room.enter_room(user_id,req)
    if game_flow.ws_send_data_to_room_handler:
        await game_flow.ws_send_data_to_room_handler(data.get("room_id"),res)
async def handle_exit_room(data:dict,user_id:int):
    req=parse_model(data,ExitRoomRequest)
    if not req:
        raise ValueError("ExitRoomRequest Parse Failed")
    res=await room.eixt_room(req)
    if res is not None:
        print("handle_exit_room Not None")
    else:
        print("handle_exit_room Is None")        
    if game_flow.ws_send_data_to_room_handler:
        print(f"handle_exit_room ID: {res.room_id}")
        await game_flow.ws_send_data_to_room_handler(res.room_id,res)
    if game_flow.ws_send_data_to_user_handler:
        await game_flow.ws_send_data_to_user_handler(user_id,res)
