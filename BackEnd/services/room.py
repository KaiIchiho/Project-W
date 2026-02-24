from schemas.room import ExitRoomRequest,ExitRoomResponse,EnterRoomRequest,EnterRoomResponse,CreateRoomRequest,CreateRoomResponse
from schemas.global_registration import players,rooms,player_room
from core.room import Room

def get_room_id_list():
    room_id_list=list(rooms.keys())
    return room_id_list
    
def create_room(req:CreateRoomRequest):
    room_id=req.room_id
    if rooms.get(room_id) is not None:
        return CreateRoomResponse(ok=False,room_id=room_id)
    rooms[room_id]=Room(room_id)
    return CreateRoomResponse(ok=True,room_id=room_id)

def enter_room(req:EnterRoomRequest):
    if player_room.get(req.user_id) is not None:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)

    room=rooms.get(req.room_id)
    if room is None:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)
    if room.check_user_in_room(req.user_id)==True:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)
    if room.room_id != req.room_id:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)
    
    print(f"Enter Room, RoomID: {req.room_id}, UserID: {req.user_id}, IsPlayer: {req.as_player}")
    player=players.get(req.user_id)
    if player is None:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)

    result=None
    if req.as_player:
        result=room.entered_as_player(player)
    else:
        result=room.enter_as_viewer(player)
    if result==True:
        player_room[req.user_id]=req.room_id
    return EnterRoomResponse(ok=result,user_id=req.user_id,room_id=req.room_id)
    
def eixt_room(req:ExitRoomRequest):
    return exit_room_by_id(req.user_id)

def exit_room_by_id(user_id:str)->ExitRoomResponse:
    room_id=player_room.get(user_id)
    if room_id is None:
        return ExitRoomResponse(ok=False,detail="player is not in any room",user_id=user_id)
    
    room=rooms.get(room_id)
    if room is None:
        return ExitRoomResponse(ok=False,detail="room is None",user_id=user_id)
    result=room.exit_by_id(user_id)
    if result==True:
        player_room.pop(user_id)
    return ExitRoomResponse(ok=result,detail="exit result",user_id=user_id)    