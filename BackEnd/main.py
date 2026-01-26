from fastapi import FastAPI,WebSocket,WebSocketDisconnect
import asyncio
from .core.room import Room
from typing import Optional
from .models.player import Player
from .services.connection import Connection

app=FastAPI()

@app.get("/api/hello")
def root():
    a=step_one()
    b=step_two()
    return {"Message" : "BackEnd Is Running!", "a" : a, "b" : b}

def step_one():
    return "one"

def step_two():
    return "two"

def test_game_flew():
    return "test"

# Connected Clients List
connected_clients:list[WebSocket]=[]

@app.websocket("/ws")
async def websocket_endpoint(ws:WebSocket):
    await ws.accept()
    # Add ws To Connected Clients List
    connected_clients.append(ws)
    print("New client connected. Total:", len(connected_clients))
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
    
    
players:dict[str,Player]={}
connections:dict[str,Connection]={}
test_room:Room=Room()

@app.post("/login")
def login(user_id:str,ws:WebSocket):
    player=Player("player_1",user_id,"Player1",None)
    print(f"Player Create Successed , User ID={user_id}")
    connection=Connection(user_id,ws)
    print(f"connection Create Successed , User ID={user_id}")
    players[user_id,player]
    print(f"Player Mapping Successed , User ID={user_id}")
    connections[user_id,connection]
    print(f"connection Mapping Successed , User ID={user_id}")

@app.post("/enter_room")
def enter_room_test():
    if Room is None:
        return
    #Room.set_player_1()