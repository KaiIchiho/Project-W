from fastapi import APIRouter
from schemas.deck_card_info import DeckListRequest,DeckListResponse
from services import deck_card_info

router=APIRouter()

@router.post("/deck_list",response_model=DeckListResponse)
def deck_list(req:DeckListRequest):
    return deck_card_info.deck_list(req)
