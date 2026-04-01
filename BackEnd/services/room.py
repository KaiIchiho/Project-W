from schemas.room import ExitRoomRequest,ExitRoomResponse,EnterRoomRequest,EnterRoomResponse
from schemas.global_registration import players,rooms,user_room,room_game
from core.room import Room
from db import room_repo

USE_DB=False

def init_rooms():
    print("Rooms Initialize")
    room_datas=room_repo.read_all_rooms()
    for room_data in room_datas:
        room_id=room_data.get("id")
        room_name=room_data.get("name")
        if not room_id or not room_name:
            continue
        result=_create_room_instance(room_id,room_name)
        if result:
            print(f"ID: {room_id}, Name: {room_name}, Successed")
        else:
            print(f"ID: {room_id}, Name: {room_name}, Failed")

def get_room_id_list():
    room_id_list=list(rooms.keys())
    return room_id_list
    
# def create_room(req:CreateRoomRequest):
#     room_id=req.room_id
#     room_name=req.room_name
    
#     # Instance
#     result=_create_room_instance(room_id,room_name)
#     if not result:
#         return CreateRoomResponse(
#             success=result,room_id=req.room_id,room_name=room_name,
#             log=f"{room_id} のルーム作成が成功できませんでした")
    
#     # Dont Use DB
#     if not USE_DB:
#         return CreateRoomResponse(
#             success=result,room_id=req.room_id,room_name=room_name,
#             log=f"{room_id} のルーム作成が成功しました")
    
#     # DB
#     result=room_repo.insert_room_data(req.room_id,req.room_name)
#     if not result:
#         rooms.pop(req.room_id)
#         return CreateRoomResponse(
#             success=result,room_id=req.room_id,room_name=room_name,
#             log=f"{room_id} のルーム作成が成功できませんでした")
#     return CreateRoomResponse(
#         success=result,room_id=req.room_id,room_name=room_name,
#         log=f"{room_id} のルーム作成が成功しました")

def _create_room_instance(room_id:int,room_name:str)->bool:
    if rooms.get(room_id) is not None:
        return False
    rooms[room_id]=Room(room_id,room_name)
    return True

def enter_room(user_id:int,req:EnterRoomRequest)->EnterRoomResponse:
    room_id=req.room_id
    is_player=req.user_is_player
    
    # Check If User ID is Valid
    print(f"Enter Room, RoomID: {room_id}, UserID: {user_id}, IsPlayer: {is_player}")
    player=players.get(user_id)
    if player is None:
        return EnterRoomResponse(
            event=req.event,
            room_id=room_id,
            user_id=user_id,
            success=False,
            user_is_player=req.user_is_player,
            log=f"{user_id}のユーザーが存在しません")
    
    # Check If User is In Room
    if user_room.get(user_id) is not None:
        return EnterRoomResponse(
            event=req.event,
            room_id=room_id,
            user_id=user_id,
            success=False,
            user_is_player=req.user_is_player,
            log=f"{user_id}のユーザーは既に在室中です")

    # Check If Room ID is Valid
    room=rooms.get(room_id)
    if room is None:
        return EnterRoomResponse(
            event=req.event,
            room_id=room_id,
            user_id=user_id,
            success=False,
            user_is_player=req.user_is_player,
            log=f"{room_id}のルームが存在しません")
    # Check If User is In Target Room
    if room.check_user_in_room(user_id)==True:
        return EnterRoomResponse(
            event=req.event,
            room_id=room_id,
            user_id=user_id,
            success=False,
            user_is_player=req.user_is_player,
            log=f"{user_name} が既にルーム{room_name}に在室です")
    # Check If Room's ID is Correct
    if room.room_id != room_id:
        return EnterRoomResponse(
            event=req.event,
            room_id=room_id,
            user_id=user_id,
            success=False,
            user_is_player=req.user_is_player,
            log=f"ルームID{room_id}は間違っています")
    
    # Enter Room
    result=None
    user_name=player.name
    room_name=room.room_name
    log=None
    if is_player:
        result=room.entered_as_player(player)
    else:
        result=room.enter_as_viewer(player)
    
    # Result
    if result==True:
        user_room[user_id]=room_id
        log=f"{user_name} がルーム{room_name}に入室しました"
    else:
        log=f"{user_name} がルーム{room_name}に入室できませんでした"
        
    return EnterRoomResponse(
            event=req.event,
            room_id=room_id,
            user_id=user_id,
            success=result,
            user_is_player=req.user_is_player,
            log=log)
    
async def eixt_room(req:ExitRoomRequest):
    return await exit_room_by_id(req.user_id,req.event)

async def exit_room_by_id(user_id:int,event:str="")->ExitRoomResponse:
    # Check If User ID is Valid
    player=players.get(user_id)
    if player is None:
        return ExitRoomResponse(
            event=event,
            room_id=-1,
            user_id=user_id,
            success=False,
            log=f"{user_id}のユーザーが存在しません")
    
    # Check If User is In Room And Get Room ID
    room_id=user_room.get(user_id)
    if room_id is None:
        return ExitRoomResponse(
            event=event,
            room_id=-1,
            user_id=user_id,
            success=False,
            log=f"{user_id} のユーザーは在室ではありません")
    
    # Check If Room ID is Valid
    room=rooms.get(room_id)
    if room is None:
        return ExitRoomResponse(
            event=event,
            room_id=room_id,
            user_id=user_id,
            success=False,
            log=f"在室中の {room_id} のルームが存在しません")
    
    # Result
    result=room.exit_by_id(user_id)
    user_name=player.name
    room_name=room.room_name
    log=None    
    if result==True:
        log=f"{user_name} がルーム{room_name}を退室しました"
        user_room.pop(user_id,None)
        print("Exit Room.")
        game=room_game.get(room_id)
        if game:
            await game.forced_game_end()
            room_game.pop(room_id,None)
            print("Game End.")
    else:
        log=f"{user_name} がルーム{room_name}を退室できませんでした"        
    
    return ExitRoomResponse(
        event=event,
        room_id=room_id,
        user_id=user_id,
        success=result,
        log=log)