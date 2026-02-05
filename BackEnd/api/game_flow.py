from fastapi import APIRouter
from api.router import router_api

router=APIRouter()

@router.post("/standby")
def standby():
    
    return
