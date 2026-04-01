from fastapi import WebSocket,WebSocketDisconnect
from starlette.websockets import WebSocketState
from pydantic import BaseModel
import asyncio
import time
import json
from core.room import Room
from models.player import Player
from services.connection import Connection
from schemas.global_registration import connections,connected_clients,rooms,user_room
from services import game_flow,login_logout
from config.setting import WS_TIMEOUT

async def websocket(ws:WebSocket):
    await ws.accept()
    
    # First : client send user_id
    user_id_text = await ws.receive_text()
    user_id=_switch_str_to_int(user_id_text)
    if user_id is None:
        ws.send_text("User ID must be an integer.")
        return
    # Add ws To Connected Clients List
    connected_clients.append(ws)
    print("New client connected. Total:", len(connected_clients))
    connections[user_id]=Connection(user_id,ws)
    print(f"WebSocket bound to user: {user_id}")
    
    # Initialize Timeout
    last_active=time.time()
    try:
        while True:
            #msg=await ws.receive()
            #Timeout
            try:
                # print("Log: Wait For WebSocket Receive.")
                msg=await asyncio.wait_for(ws.receive(),timeout=1)
            except asyncio.TimeoutError:
                # print("Error: WebSocket Receive TimeoutError.")
                msg=None
            if msg:    
                print(f"Log: WebSocket message is {msg}")
                if msg["type"]=="websocket.disconnect":
                    break
                if msg["type"]=="websocket.receive":
                    data=msg.get("text")
                    print(f"Log: WebSocket Data is {data}")
                    if data!="ping":
                        last_active=time.time()
            if time.time()-last_active>WS_TIMEOUT:
                print("Log: WebSocket Timeout.")
                #break
                message=create_message(None,f"{user_id} Timeout.")
                await send_message(message,user_id)
                last_active=time.time()
            if msg is None:
                continue
            
            #Room Check
            room_id=user_room.get(user_id)
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
            
            #Process Message
            msg_type=await read_wsmsg_type(msg)
            if msg_type==1:
                await receive_text(ws,room,msg["text"])
            elif msg_type==2:
                await receive_json(ws,user_id,room,json.loads(msg["text"]))
    except WebSocketDisconnect:
        print("Client disconnected.")
    finally:
        print("Log: WebSocket Finally.")
        await login_logout.logout_by_id(user_id)

def _switch_str_to_int(string:str)->int:
    try:
        intager=int(string)
        return intager
    except ValueError as e:
        # raise ValueError("User ID must be an integer.") from e
        return None

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
        await connect.websocket.send_text(f"From Server -\n {text}")
            
    await ws.send_text(f"From Server -\n (yourself){text}")
    
async def receive_json(ws:websocket,user_id:int,room:Room,json:dict):
    # command=json.get("type")
    # if command is None:
    #     print("Error: JSON Command Is None !")
    #     return
    
    # if command=="standby":
    #     await game_flow.standby(user_id)
    # else:
    #     await game_flow.receive_command_json(room.room_id,json,user_id)
    print("Received JSON: ",json)
    if json.get("event") is None:
        # await game_flow.standby(user_id)
        await game_flow.handle_outgame_event(json,user_id)
    else:
        await game_flow.receive_command_json(room.room_id,json,user_id)

def create_message(self_text:str,room_text:str)->dict:
    message={}
    message["self"]=self_text
    message["room"]=room_text
    return message

async def send_message(message:dict,user_id:int):
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
    
    room_id=user_room.get(user_id)
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

async def send_data_to_user(target_user_id:int,data:BaseModel):
    connection=connections.get(target_user_id)
    if not connection:
        return
    ws=connection.websocket
    if not ws:
        return
    if ws.application_state == WebSocketState.CONNECTED:
        ws.send_json(data.dict())

async def send_data_to_room(room_id:int,data:BaseModel):
    room=rooms.get(room_id)
    if not room:
        return
    user_ids:list[int]=None
    if room.player_1:
        user_ids.append(room.player_1.player_id)
    if room.player_2:
        user_ids.append(room.player_2.player_id)
    if room.viewer:
        user_ids.append(room.viewer.player_id)
    for user_id in user_ids:
        await send_data_to_user(user_id,data)
        
async def send_data_to_room_except_target(room_id:int,target_user_id:int,data:BaseModel):
    room=rooms.get(room_id)
    if not room:
        return
    user_ids:list[int]=None
    if room.player_1 and room.player_1.player_id!=target_user_id:
        user_ids.append(room.player_1.player_id)
    if room.player_2 and room.player_2.player_id!=target_user_id:
        user_ids.append(room.player_2.player_id)
    if room.viewer and room.viewer.player_id!=target_user_id:
        user_ids.append(room.viewer.player_id)
    for user_id in user_ids:
        await send_data_to_user(user_id,data)

game_flow.ws_send_message_handler=send_message
game_flow.create_message_handler=create_message
game_flow.ws_send_data_to_user_handler=send_data_to_user
game_flow.ws_send_data_to_room_handler=send_data_to_room
game_flow.ws_send_data_to_room_except_target_handler=send_data_to_room_except_target