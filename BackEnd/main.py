from fastapi import FastAPI,APIRouter
from api.router import api_router
from services.startup import on_startup
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app=FastAPI()

# テスト用のフロントエンド
app.mount("/static", StaticFiles(directory="testclient"), name="static")
# app.mount("/static", StaticFiles(directory="client"), name="static")
# @app.get("/testclient")
# async def get():
#     with open("testclient/test-frontend.html") as f:
#         return HTMLResponse(f.read())
@app.get("/{client_root}", response_class=HTMLResponse)
async def get(client_root:str):
    routes = {
        "testclient": "testclient/test-frontend.html",
        # "client":""
    }
    url = routes.get(client_root)
    if not url:
        return HTMLResponse("Not Found", status_code=404)
    return FileResponse(url)

# サーバー起動時点で呼び出す
@app.on_event("startup")
async def startup():
    print("Log: Server Startup.")
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


