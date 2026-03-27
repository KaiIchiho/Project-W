from fastapi import WebSocket
from models.player import Player
from core.room import Room
from core.game import Game
from services.connection import Connection

# Connected Clients List
connected_clients:list[WebSocket]=[]

players:dict[int,Player]={}
connections:dict[int,Connection]={}
#test_room:Room=Room("test_room_01")
rooms:dict[int,Room]={}
user_room:dict[int,int]={}

room_game:dict[int,Game]={}