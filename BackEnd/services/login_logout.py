from schemas.login_logout import LoginRequest,LoginResponse,LogoutRequest,LogoutResponse
from schemas.global_registration import players,connections,player_room,rooms
from models.player import Player
from services.connection import Connection
from services.room import exit_room_by_id

def login(req: LoginRequest):
    user_id=req.user_id
    user_name=req.user_name
    player=Player(user_id,user_id,user_name,None)
    players[user_id]=player
    print(f"Player Create Successed , UserID={user_id}, UserName={user_name}")
    return LoginResponse(ok=True, user_id=user_id,user_name=user_name)

async def logout(req:LogoutRequest):
    user_id=req.user_id
    
    #player
    player=players.get(user_id)
    if player:
        players.pop(user_id)
    
    #room
    exit_room_by_id(user_id)
    
    #websocket    
    connection=connections.get(user_id)
    if connection:
        await connection.websocket.close(code=1000)
        connections.pop(user_id)
    
    return LogoutResponse(ok=True)