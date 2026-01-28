from fastapi import FastAPI,APIRouter,WebSocket,WebSocketDisconnect
from pydantic import BaseModel
import asyncio
from typing import Optional
from core.room import Room
from models.player import Player
from services.connection import Connection

app=FastAPI()

api = APIRouter(prefix="/api")

@api.get("/hello")
def root():
    return {"Message" : "BackEnd Is Running!"}
def test_game_flew():
    return "test"

# Connected Clients List
connected_clients:list[WebSocket]=[]

players:dict[str,Player]={}
connections:dict[str,Connection]={}
test_room:Room=Room("test_room_01")

class LoginRequest(BaseModel):
    user_id:str
    user_name:str
class LoginResponse(BaseModel):
    ok:bool
    user_id:str
    user_name:str
class LogoutRequest(BaseModel):
    user_id:str
class LogoutResponse(BaseModel):
    ok:bool
    
class EnterRoomRequest(BaseModel):
    room_id:str
    user_id:str
    as_player:bool
class EnterRoomResponse(BaseModel):
    ok:bool
    room_id:str
    user_id:str
class ExitRoomRequest(BaseModel):
    room_id:str
    user_id:str
class ExitRoomResponse(BaseModel):
    ok:bool
    detail:str
    user_id:str
    
@app.websocket("/ws")
async def websocket_endpoint(ws:WebSocket):
    await ws.accept()
    # Add ws To Connected Clients List
    connected_clients.append(ws)
    print("New client connected. Total:", len(connected_clients))
    
    # First : client send user_id
    user_id = await ws.receive_text()
    connections[user_id]=ws
    print(f"WebSocket bound to user: {user_id}")
    
    try:
        while True:
            data=await ws.receive_text()
            print("Received : ",data)
            
            # Broadcast to other clients
            for client in connected_clients.copy():
                print("client id:", id(client), "ws id:", id(ws))
                try:
                    if client is ws:
                        continue
                    await client.send_text(f"From Server - {data}")
                except Exception:
                    connected_clients.remove(client)
                    
            await ws.send_text(f"From Server - (yourself){data}")
            #asyncio.create_task(ws.send_text(f"(yourself){data}"))
    except WebSocketDisconnect:
        # Remove ws From Connected Clients List
        connected_clients.remove(ws)
        connections.pop(user_id)
        print("Client disconnected. Total:", len(connected_clients))
    
@api.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    user_id=req.user_id
    user_name=req.user_name
    player=Player(user_id,user_id,user_name,None)
    players[user_id]=player
    print(f"Player Create Successed , UserID={user_id}, UserName={user_name}")
    return LoginResponse(ok=True, user_id=user_id,user_name=user_name)
@api.post("/logout",response_model=LogoutResponse)
def logout(req:LogoutRequest):
    user_id=req.user_id
    players.pop(user_id)
    return LogoutResponse(ok=True)

@api.post("/enter_room",response_model=EnterRoomResponse)
def enter_room(req:EnterRoomRequest):
    if test_room is None:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)
    if test_room.room_id != req.room_id:
        print 
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)
    player=players.get(req.user_id)
    if player is None:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)

    result=None
    if req.as_player:
        result=test_room.entered_as_player(player)
    else:
        result=test_room.enter_as_viewer(player)
    return EnterRoomResponse(ok=result,user_id=req.user_id,room_id=req.room_id)
    
@api.post("/exit_room",response_model=ExitRoomResponse)
def eixt_room(req:ExitRoomRequest):
    if test_room is None:
        return ExitRoomResponse(ok=False,detail="test_room is None")
    #result=test_room.exit_by_id(req.user_id)
    return ExitRoomResponse(ok=result,detail="exit result")
    
app.include_router(api)