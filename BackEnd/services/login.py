from schemas.login import LoginRequest,LoginResponse,LogoutRequest,LogoutResponse
from schemas.global_registration import players
from models.player import Player

def login(req: LoginRequest):
    user_id=req.user_id
    user_name=req.user_name
    player=Player(user_id,user_id,user_name,None)
    players[user_id]=player
    print(f"Player Create Successed , UserID={user_id}, UserName={user_name}")
    return LoginResponse(ok=True, user_id=user_id,user_name=user_name)

def logout(req:LogoutRequest):
    user_id=req.user_id
    players.pop(user_id)
    return LogoutResponse(ok=True)