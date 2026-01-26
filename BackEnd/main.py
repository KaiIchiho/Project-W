from fastapi import FastAPI,APIRouter,WebSocket,WebSocketDisconnect
from pydantic import BaseModel
import asyncio
from typing import Optional
from core.room import Room
from models.player import Player
from services.connection import Connection

app=FastAPI()

api = APIRouter(prefix="/api")

@app.get("/hello")
def root():
    return {"Message" : "BackEnd Is Running!"}
def test_game_flew():
    return "test"

# Connected Clients List
connected_clients:list[WebSocket]=[]

players:dict[str,Player]={}
connections:dict[str,Connection]={}
test_room:Room=Room()

class LoginRequest(BaseModel):
    user_id:str
class LoginResponse(BaseModel):
    ok:bool
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
        print("Client disconnected. Total:", len(connected_clients))
    
@app.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    print(f"Player Create Successed , User ID={user_id}")
    user_id=req.user_id
    
    player=Player("player_1",user_id,"Player1",None)
    players[user_id]=player
    
    print(f"Player created: {user_id}")
    return LoginResponse(True,user_id)

@app.post("/enter_room")
def enter_room_test():
    if Room is None:
        return
    #Room.set_player_1()
    
    
app.include_router(api)