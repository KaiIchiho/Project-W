from fastapi import APIRouter
from schemas.room import ExitRoomRequest,ExitRoomResponse,EnterRoomRequest,EnterRoomResponse,CreateRoomRequest,CreateRoomResponse
from services import room

router=APIRouter()

@router.get("/get_room_id_list")
def get_room_id_list_endpoint():
    return room.get_room_id_list()
    
@router.post("/create_room",response_model=CreateRoomResponse)
def create_room_endpoint(req:CreateRoomRequest):
    return room.create_room(req)

@router.post("/enter_room",response_model=EnterRoomResponse)
def enter_room_endpoint(req:EnterRoomRequest):
    return room.enter_room(req)
    
@router.post("/exit_room",response_model=ExitRoomResponse)
def eixt_room_endpoint(req:ExitRoomRequest):
    return room.eixt_room(req)