from fastapi import APIRouter
from api.router import router_api

router=APIRouter(prefix=router_api)

@router.post("/standby")
def standby():
    
    return
