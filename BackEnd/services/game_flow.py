from core.game import Game
from core.room import Room
from schemas import global_registration
from typing import Callable,Awaitable
from pydantic import BaseModel
# from typing import Optional
import importlib

ws_send_message_handler:Callable[[dict,str],Awaitable[None]]
create_message_handler:Callable[[int,str],dict]

ws_send_data_to_user_handler:Callable[[int,BaseModel],Awaitable[None]]
ws_send_data_to_room_handler:Callable[[int,BaseModel],Awaitable[None]]
ws_send_data_to_room_except_target_handler:Callable[[int,int,BaseModel],Awaitable[None]]

outgame_handlers={
        "enter_room":"handle_enter_room",
        "exit_room":"handle_exit_room",
        "standby":"handle_standby",
        "deck_list":"handle_deck_list",
        }

async def handle_outgame_event(data:dict,user_id:int):
    print("handle_outgame_event")
    handler_name=outgame_handlers.get(data.get("event"))
    if not handler_name:
        raise ValueError("Action Not Found")
    module = importlib.import_module("services.outgame_handle")
    handler = getattr(module, handler_name, None)
    # handler=globals().get(handler_name)
    print("event:", handler_name)
    print("handler:", handler)
    await handler(data,user_id)
  
async def standby(user_id:int)->int:
    player=global_registration.players.get(user_id)
    room_id=global_registration.player_room.get(user_id)
    if room_id is None:
        raise ValueError(f"{user_id} User Is Not In Room")
        #return -1
    room=global_registration.rooms.get(room_id)
    if room is None:
        raise ValueError(f"{room_id} Room Not Found")
        #return -1
    
    game=_create_game_instance(room)
    result=await game.set_player_to_none(player,game.start_game)
    return result
    
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

async def receive_command_json(room_id:int,command_json:dict,user_id:int):
    action=command_json.get("action")
    print(f"Log: Command Type Is {action}")
    game=get_game_by_room_id(room_id)
    if game is None:
        return #"Error !"
    await game.handle_action(command_json,user_id)