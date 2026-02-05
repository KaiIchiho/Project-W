from fastapi import APIRouter
from schemas.room import ExitRoomRequest,ExitRoomResponse,EnterRoomRequest,EnterRoomResponse,CreateRoomRequest,CreateRoomResponse
from services import room

router=APIRouter()

@router.get("/get_room_id_list")
def get_room_id_list():
    return room.get_room_id_list()
    
@router.post("/create_room",response_model=CreateRoomResponse)
def create_room(req:CreateRoomRequest):
    return room.create_room(req)

@router.post("/enter_room",response_model=EnterRoomResponse)
def enter_room(req:EnterRoomRequest):
    return room.enter_room(req)
    
@router.post("/exit_room",response_model=ExitRoomResponse)
def eixt_room(req:ExitRoomRequest):
    return room.eixt_room(req)