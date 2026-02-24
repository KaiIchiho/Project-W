from fastapi import WebSocket,WebSocketDisconnect
from starlette.websockets import WebSocketState
import json
from core.room import Room
from models.player import Player
from services.connection import Connection
from schemas.global_registration import connections,connected_clients,rooms,player_room
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
            
            #Room Check
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
                await receive_json(ws,user_id,room,json.loads(msg["text"]))
            
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
            await connect.websocket.send_text(f"From Server -\n {text}")
        except WebSocketDisconnect:
            connections.pop(uid)
            
    await ws.send_text(f"From Server -\n (yourself){text}")
    #asyncio.create_task(ws.send_text(f"(yourself){text}"))
    
async def receive_json(ws:websocket,user_id:str,room:Room,json:dict):
    command=json.get("type")
    if command is None:
        print("Error: JSON Command Is None !")
        return
    
    if command=="standby":
        await game_flow.standby(user_id)
    else:
        await game_flow.receive_command_json(room.room_id,json,user_id)

async def send_message(message:dict,user_id:str):
    if user_id is None:
        return
    present_text="From Server - "
    self_connection=connections.get(user_id)
    self_ws=None
    if self_connection is not None:
        self_ws=self_connection.websocket
    to_self=message.get("self")
    to_room=message.get("room")
    if self_ws is not None and to_self is not None:
        if self_ws.application_state == WebSocketState.CONNECTED:
            await self_ws.send_text(present_text+to_self)
    
    room_id=player_room.get(user_id)
    if room_id is None:
        return
    room=rooms.get(room_id)
    if room is None or to_room is None:
        return
    await send_message_by_player(room.player_1,present_text+to_room)
    await send_message_by_player(room.player_2,present_text+to_room)
    await send_message_by_player(room.viewer,present_text+to_room)
    
async def send_message_by_player(player:Player,message:str):
    if player is None:
        return
    connection=connections.get(player.player_id)
    if connection is None:
        return
    ws=connection.websocket
    if ws is None:
        return
    if ws.application_state == WebSocketState.CONNECTED:
        await ws.send_text(message)
    
game_flow.ws_send_handler=send_message