from fastapi import APIRouter
from api import websocket,room,game_flow,login_logout

router_api="/api"
api_router=APIRouter(prefix=router_api)

api_router.include_router(websocket.router)
api_router.include_router(login_logout.router)
api_router.include_router(room.router)
api_router.include_router(game_flow.router)