from fastapi import WebSocket
from models.player import Player
from core.room import Room
from services.connection import Connection

# Connected Clients List
connected_clients:list[WebSocket]=[]

players:dict[str,Player]={}
connections:dict[str,Connection]={}
#test_room:Room=Room("test_room_01")
rooms:dict[str,Room]={}
player_room:dict[str,str]={}