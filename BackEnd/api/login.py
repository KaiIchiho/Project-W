from fastapi import APIRouter
from schemas.login import LoginRequest,LoginResponse,LogoutRequest,LogoutResponse
from services import login

router=APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    return login.login(req)

@router.post("/logout",response_model=LogoutResponse)
def logout(req:LogoutRequest):
    return login.logout(req)