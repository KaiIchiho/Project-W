from fastapi import APIRouter
from api import websocket,login,room,game_flow

router_api="/api"
api_router=APIRouter(prefix=router_api)

api_router.include_router(websocket.router)
api_router.include_router(login.router)
api_router.include_router(room.router)
api_router.include_router(game_flow.router)