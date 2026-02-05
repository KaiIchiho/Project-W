from fastapi import APIRouter,WebSocket
from api.router import router_api
from services import websocket

router=APIRouter()

#@app.websocket("/ws")
@router.websocket("/ws")
async def websocket_endpoint(ws:WebSocket):
    websocket.websocket_endpoint(ws)