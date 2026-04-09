from core.game import Game
from core.room import Room
from schemas import global_registration
from typing import Callable,Awaitable
from schemas.game_flow import SelectDeckResponse,StandbyResponse
from pydantic import BaseModel
import importlib
from services.login_logout import get_logedin_user_name
from schemas import event_type
from db.deck_repo import read_deck_name_by_id

ws_send_message_handler:Callable[[dict,str],Awaitable[None]]
create_message_handler:Callable[[int,str],dict]

ws_send_data_to_user_handler:Callable[[int,BaseModel],Awaitable[None]]
ws_send_data_to_room_handler:Callable[[int,BaseModel],Awaitable[None]]
ws_send_data_to_room_except_target_handler:Callable[[int,int,BaseModel],Awaitable[None]]

outgame_handlers={
        event_type.ENTER_ROOM:"handle_enter_room",
        event_type.EXIT_ROOM:"handle_exit_room",
        event_type.SELECT_DECK:"handle_select_deck",
        event_type.STANDBY:"handle_standby",
        # event_type.:"handle_deck_list",
        }

async def handle_outgame_event(data:dict,user_id:int):
    print("handle_outgame_event")
    event=outgame_handlers.get(data.get("event"))
    if not event:
        raise ValueError("Action Not Found")
    module = importlib.import_module("services.outgame_handle")
    handler = getattr(module, event, None)
    # handler=globals().get(event)
    print("event:", event)
    print("handler:", handler)
    await handler(data,user_id)
  
async def set_player_deck(user_id:int,deck_id:int):
    success=False
    log=""
    
    room_id=global_registration.user_room.get(user_id)
    if room_id is not None:
        game=global_registration.room_game.get(room_id)
        if game and game.get_is_in_progress():
            log="ゲーム進行中"
            res=SelectDeckResponse(
                success=success,
                log=log
            )
            return res
    
    player=global_registration.players.get(user_id)
    if player:
        deck_name=read_deck_name_by_id(deck_id)
        if deck_name is None:
            log=f"{deck_id}のデッキが存在しません"
        else:
            success=player.set_deck_id(deck_id)
            user_name=get_logedin_user_name(user_id)
            if success:
                log=f"{user_name}は{deck_name}(ID:{deck_id})のデッキを選択しました"
            else:
                log=f"{user_name}は{deck_name}(ID:{deck_id})のデッキを選択できませんでした"
    else:
        log=f"{user_id}のプレイヤーが存在しません"
    
    res=SelectDeckResponse(
        success=success,
        log=log
    )
    return res

async def standby(user_id:int):
    player=global_registration.players.get(user_id)
    room_id=global_registration.user_room.get(user_id)
    success=False
    log=""
    game=None
    user_name=get_logedin_user_name(user_id)
    if player is not None and room_id is not None:
        room=global_registration.rooms.get(room_id)
        if room is not None:    
            game=_create_game_instance(room)
            
            has_standby=game.check_player_identity_by_id(user_id)
            
            if has_standby==-1:
                result=await game.set_player_to_none(player)
                if result!=-1:
                    success=True
                    log=f"{user_name}が対戦開始の準備が整えました"
                else:
                    success=False
                    log=f"{user_name}が対戦開始の準備が失敗しました"
            else:
                result=game.cancel_set_player(user_id)
                if result!=-1:
                    success=True
                    log=f"{user_name}が対戦開始の準備が取り消しました"
                else:
                    success=False
                    log=f"{user_name}が対戦開始の準備が取り消し失敗しました"
    res=StandbyResponse(
        success=success,
        log=log
    )
    return res,game
    
    
def _create_game_instance(room:Room)->Game:
    room_id=room.room_id
    game=get_game_by_room_id(room_id)
    if game is not None:
        print(f"Log: {room_id} Room Has GameInstance")
    else:
        game=Game(room_id)
        # delegate
        game.ws_send_message=ws_send_message_handler
        game.create_message=create_message_handler
        game.ws_send_data_to_user=ws_send_data_to_user_handler
        game.ws_send_data_to_room=ws_send_data_to_room_handler
        game.ws_send_data_to_room_except_target=ws_send_data_to_room_except_target_handler
        global_registration.room_game[room_id]=game
    return game
    
def get_game_by_room_id(room_id:int)->Game:
    return global_registration.room_game.get(room_id)

def get_room_id_by_user_id(user_id:int)->int:
    room_id=global_registration.user_room.get(user_id)
    if room_id is None:
        return -1
    else:
        return room_id

async def receive_ingame_command(data:dict,user_id:int):
    room_id=get_room_id_by_user_id(user_id)
    game=get_game_by_room_id(room_id)
    if game is None:
        return
    common=data.get("client_common")
    event=common.get("event")
    await game.handle_action(data,event,user_id)
    
async def start_game(game:Game,player_id:int):
    await game.start_game(player_id)