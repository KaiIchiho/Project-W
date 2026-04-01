from fastapi import APIRouter
from schemas.deck_card_info import DeckListRequest,DeckListResponse,SelectDeckResquest,SelectDeckResponse
from services import deck_card_info

router=APIRouter()

@router.post("/deck_list",response_model=DeckListResponse)
def deck_list_endpoint(req:DeckListRequest):
    return deck_card_info.deck_list(req)

@router.post("/select_deck",response_model=SelectDeckResponse)
def select_deck_endpoint(req:SelectDeckResquest):
    #return deck_card_info.deck_list(req)
    pass