from core.game import Game
from core.room import Room
from schemas import global_registration

def standby(user_id:str)->bool:
    room_id=global_registration.player_room.get(user_id)
    if room_id is None:
        print(f"Error: {user_id} User Is Not In Room")
        return False
    return create_game_instance(room_id)

def next_phase():
    return

def next_turn():
    return

def create_game_instance(room_id:str)->bool:
    room=global_registration.rooms.get(room_id)
    if room is None:
        print(f"Error: {room_id} Room Not Found")
        return False
    game=global_registration.room_game.get(room_id)
    if game is not None:
        print(f"Error: {room_id} Room Has GameInstance")
        return False
    if room.check_is_players_full()==False:
        print(f"Warning: {room_id} Room Has Not Players Full")
        return False
    
    game=Game(room.player_1,room.player_2,room.player_1)
    global_registration.room_game[room_id]=game
    return True
    