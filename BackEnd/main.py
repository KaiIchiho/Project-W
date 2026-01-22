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

@app.get("/api/ws")
async def websocket_endpoint(ws:WebSocket):
    await ws.accept()
    try:
        while True:
            data=await ws.receive_text()
            print("Received : ",data)
            await ws.send_text(f"Echo : {data}")
    except WebSocketDisconnect:
        print("Client disconnected")