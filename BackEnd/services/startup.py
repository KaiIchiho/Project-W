from db import connection_pool
from services import room

async def on_startup():
    connection_pool.init_pool()
    room.init_rooms()