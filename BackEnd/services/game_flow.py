from core.game import Game
from core.room import Room
from schemas import global_registration

def standby(user_id:str)->int:
    player=global_registration.players.get(user_id)
    room_id=global_registration.player_room.get(user_id)
    if room_id is None:
        print(f"Warning: {user_id} User Is Not In Room")
        return -1
    room=global_registration.rooms.get(room_id)
    if room is None:
        print(f"Warning: {room_id} Room Not Found")
        return -1
    
    game=create_game_instance(room)
    result=game.set_player_to_none(player)
    if result==-1:
        print(f"Warning: Game Instance is Players Full !")
    return result

def create_game_instance(room:Room)->Game:
    room_id=room.room_id
    game=get_game_by_room_id(room_id)
    if game is not None:
        print(f"Log: {room_id} Room Has GameInstance")
    else:
        game=Game()
        global_registration.room_game[room_id]=game
    return game
    
def get_game_by_room_id(room_id:str)->Game:
    return global_registration.room_game.get(room_id)

def receive_command_json(room_id:str,command_json:dict):
    type=command_json.get("type")
    print(f"Log: Command Type Is {type}")
    game=get_game_by_room_id(room_id)
    if game is None:
        return "Error !"
    return game.handle_action(command_json)