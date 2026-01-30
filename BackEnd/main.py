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
#test_room:Room=Room("test_room_01")
rooms:dict[str,Room]={}
player_room:dict[str,str]={}

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

class CreateRoomRequest(BaseModel):
    room_id:str
class CreateRoomResponse(BaseModel):
    ok:bool
    room_id:str
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
    connections[user_id]=Connection(user_id,ws)
    print(f"WebSocket bound to user: {user_id}")
    
    try:
        while True:    
            data=await ws.receive_text()
            print("Received : ",data)
            
            room_id=player_room.get(user_id)
            if room_id is None:
                continue
            room=rooms.get(room_id)
            if room is None:
                continue
            
            is_client_in_room=room.check_player_in_room(user_id)
            if is_client_in_room==False:
                print("Client Is Not In Room As Player")
                continue
            
            print("Client Is In Room As Player")
            
            # Broadcast to other clients
            for uid in room.get_all_ids():
                connect=connections.get(uid)
                if connect is None:
                    continue
                if connect.websocket is ws:
                    continue
                try:
                    await connect.websocket.send_text(f"From Server - {data}")
                except WebSocketDisconnect:
                    connections.pop(uid)
                    
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

@api.get("/get_room_id_list")
def get_room_id_list():
    room_id_list=[id for id,room in rooms]
    return room_id_list
    
@api.post("/create_room",response_model=CreateRoomResponse)
def create_room(req:CreateRoomRequest):
    room_id=req.room_id
    if rooms.get(room_id) is not None:
        return CreateRoomResponse(ok=False,room_id=room_id)
    rooms[room_id]=Room(room_id)
    return CreateRoomResponse(ok=True,room_id=room_id)

@api.post("/enter_room",response_model=EnterRoomResponse)
def enter_room(req:EnterRoomRequest):
    if player_room.get(req.user_id) is not None:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)

    room=rooms.get(req.room_id)
    if room is None:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)
    if room.check_user_in_room(req.user_id)==True:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)
    if room.room_id != req.room_id:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)
    
    print(f"Enter Room, RoomID: {req.room_id}, UserID: {req.user_id}, IsPlayer: {req.as_player}")
    player=players.get(req.user_id)
    if player is None:
        return EnterRoomResponse(ok=False,user_id=req.user_id,room_id=req.room_id)

    result=None
    if req.as_player:
        result=room.entered_as_player(player)
    else:
        result=room.enter_as_viewer(player)
    if result==True:
        player_room[req.user_id]=req.room_id
    return EnterRoomResponse(ok=result,user_id=req.user_id,room_id=req.room_id)
    
@api.post("/exit_room",response_model=ExitRoomResponse)
def eixt_room(req:ExitRoomRequest):
    room_id=player_room.get(req.user_id)
    if room_id is None:
        return ExitRoomResponse(ok=False,detail="player is not in any room",user_id=req.user_id)
    
    room=rooms.get(room_id)
    if room is None:
        return ExitRoomResponse(ok=False,detail="room is None",user_id=req.user_id)
    result=room.exit_by_id(req.user_id)
    if result==True:
        player_room.pop(req.user_id)
    return ExitRoomResponse(ok=result,detail="exit result",user_id=req.user_id)
    
app.include_router(api)