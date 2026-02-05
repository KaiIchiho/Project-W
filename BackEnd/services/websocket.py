from fastapi import WebSocket,WebSocketDisconnect
from services.connection import Connection
from schemas.global_registration import connections,connected_clients,rooms,player_room

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