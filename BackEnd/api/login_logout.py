from fastapi import APIRouter
from schemas.login_logout import LoginRequest,LoginResponse,LogoutRequest,LogoutResponse
from services import login_logout

router=APIRouter()

@router.post("/login", response_model=LoginResponse)
def login_endpoint(req: LoginRequest):
    return login_logout.login(req)

@router.post("/logout",response_model=LogoutResponse)
async def logout_endpoint(req:LogoutRequest):
    return await login_logout.logout(req)