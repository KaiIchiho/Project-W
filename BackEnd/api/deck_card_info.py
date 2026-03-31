from fastapi import APIRouter
from schemas.deck_card_info import ReadDeckRequest,ReadDeckResponse
from services import deck_card_info

router=APIRouter()

@router.post("/test_deck",response_model=ReadDeckResponse)
def test_deck(req:ReadDeckRequest):
    return deck_card_info.read_deck(req)