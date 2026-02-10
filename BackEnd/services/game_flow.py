from core.game import Game
from core.room import Room
from schemas import global_registration
from typing import Callable,Awaitable

ws_send_handler:Callable[[dict,str],Awaitable[None]]

async def standby(user_id:str)->int:
    player=global_registration.players.get(user_id)
    room_id=global_registration.player_room.get(user_id)
    if room_id is None:
        raise ValueError(f"{user_id} User Is Not In Room")
        #return -1
    room=global_registration.rooms.get(room_id)
    if room is None:
        raise ValueError(f"{room_id} Room Not Found")
        #return -1
    
    game=create_game_instance(room)
    result=await game.set_player_to_none(player,game.start_game)
    #if result==-1:
    #    print(f"Warning: Game Instance is Players Full !")
    return result
    
def create_game_instance(room:Room)->Game:
    room_id=room.room_id
    game=get_game_by_room_id(room_id)
    if game is not None:
        print(f"Log: {room_id} Room Has GameInstance")
    else:
        game=Game()
        # delegate
        game.ws_send_message=ws_send_handler
        global_registration.room_game[room_id]=game
    return game
    
def get_game_by_room_id(room_id:str)->Game:
    return global_registration.room_game.get(room_id)

async def receive_command_json(room_id:str,command_json:dict,user_id:str):
    type=command_json.get("type")
    print(f"Log: Command Type Is {type}")
    game=get_game_by_room_id(room_id)
    if game is None:
        return #"Error !"
    
    player_id=command_json.get("player_id")
    print(f"Command Player ID: {player_id}")
    await game.handle_action(command_json,user_id)