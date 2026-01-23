from fastapi import FastAPI,WebSocket,WebSocketDisconnect

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
                #if client is ws:
                #    continue
                try:
                    await client.send_text(f"(youself){data}")
                except Exception:
                    connected_clients.remove(client)
            #await ws.send_text(f"Echo : {data}")
    except WebSocketDisconnect:
        # Remove ws From Connected Clients List
        connected_clients.remove(ws)
        print("Client disconnected")
        print("Client disconnected. Total:", len(connected_clients))