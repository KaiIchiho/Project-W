from fastapi import FastAPI,APIRouter
from api.router import api_router

app=FastAPI()

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


