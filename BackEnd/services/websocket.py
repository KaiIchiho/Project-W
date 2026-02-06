from fastapi import WebSocket,WebSocketDisconnect
import json
from core.room import Room
from services.connection import Connection
from schemas.global_registration import connections,connected_clients,rooms,player_room
from services.command import Command
from services import game_flow

async def websocket(ws:WebSocket):
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
            msg=await ws.receive()
            
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
            
            msg_type=await read_wsmsg_type(msg)
            if msg_type==1:
                await receive_text(ws,room,msg["text"])
            elif msg_type==2:
                await receive_json(ws,user_id,room,json.load(msg["text"]))
            
    except WebSocketDisconnect:
        # Remove ws From Connected Clients List
        connected_clients.remove(ws)
        connections.pop(user_id)
        print("Client disconnected. Total:", len(connected_clients))
        
async def read_wsmsg_type(msg)->int:
    if "bytes" in msg:
        return 0
    
    if "text" in msg:
        text=msg["text"]
        try:
            data=json.loads(text)
        except json.JSONDecodeError:
            return 1
        return 2
    
    return -1
    
async def receive_text(ws:websocket,room:Room,text:str):
    print("Received : ",text)
    
    # Broadcast to other clients
    for uid in room.get_all_ids():
        connect=connections.get(uid)
        if connect is None:
            continue
        if connect.websocket is ws:
            continue
        try:
            await connect.websocket.send_text(f"From Server - {text}")
        except WebSocketDisconnect:
            connections.pop(uid)
            
    await ws.send_text(f"From Server - (yourself){text}")
    #asyncio.create_task(ws.send_text(f"(yourself){text}"))
    
async def receive_json(ws:websocket,user_id:str,room:Room,json:dict):
    command=json.get("type")
    if command is None:
        return
    try:
        command_type=Command(command)
    except ValueError:
        return
    
    if command_type==Command.STANDBY:
        result=game_flow.standby(user_id)
        if result==False:
            await ws.send_text("From Server - Standby Failed !")
        else:
            await ws.send_text("From Server - Standby Succeeded !")
            
    elif command_type==Command.NEXT_PHASE:
        game_flow.next_phase()
    elif command_type==Command.NEXT_TURN:
        game_flow.next_turn()