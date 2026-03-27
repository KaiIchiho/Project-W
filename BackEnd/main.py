from fastapi import FastAPI,APIRouter
from api.router import api_router
from services.startup import on_startup

app=FastAPI()

# サーバー起動時点で呼び出す
@app.on_event("startup")
async def startup():
    print("Server Startup.")
    await on_startup()

app.include_router(api_router)

#=======================================================

#import asyncio
#from typing import Optional
#from core.room import Room
#from models.player import Player
#from services.connection import Connection

#api = APIRouter(prefix="/api")

#@api.get("/hello")
#def root():
#    return {"Message" : "BackEnd Is Running!"}
#def test_game_flew():
#    return "test"
    
#app.include_router(api)
#=======================================================


