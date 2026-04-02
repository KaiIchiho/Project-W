from schemas.login_logout import LoginRequest,LoginResponse,LogoutRequest,LogoutResponse
from schemas.global_registration import players,connections
from models.player import Player
# from services.connection import Connection
from services.room import exit_room_by_id
from db import user_repo

def login(req: LoginRequest):
    #user_id=req.user_id
    user_name=req.user_name
    password=req.password
    # Database
    user_id=user_repo.check_name_and_pw(user_name,password)
    if user_id is None:
        return LoginResponse(
            success=False, user_id=-1,user_name=user_name,
            log=f"{user_name} はログインできませんでした")
    
    player=Player(user_id,user_name)
    players[user_id]=player
    print(f"Log: Login Successed, UserID={user_id}, UserName={user_name}")
    return LoginResponse(
        success=True, user_id=user_id,user_name=user_name,
        log=f"{user_name} はログインしました")

async def logout(req:LogoutRequest):
    return await logout_by_id(req.user_id)

async def logout_by_id(user_id:int):
    print("Log: logout by id: ",user_id)
    #room
    await exit_room_by_id(user_id)
    
    #player
    player=players.get(user_id)
    user_name=None
    if player:
        user_name=player.name
        players.pop(user_id)
    
    #websocket    
    connection=connections.get(user_id)
    if connection:
        # await connection.websocket.close(code=1000)
        try:
            await connection.websocket.close(code=1000)
        except RuntimeError:
            pass
        connections.pop(user_id)
    
    return LogoutResponse(
        success=True,
        log=f"{user_name} はログアウトしました")