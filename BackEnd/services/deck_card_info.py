from schemas.deck_card_info import ReadDeckRequest,ReadDeckResponse,ReadCardRequest,ReadCardResponse
from db import deck_repo

def read_deck(req:ReadDeckRequest)->ReadDeckResponse:
    deck_repo.test_read_all_deck(req.deck_id)
    return ReadDeckResponse(
        success=True,
        log="test_read_all_deck")
    
def read_card(req:ReadCardRequest)->ReadCardResponse:
    deck_repo.test_read_all_card()
    return ReadCardResponse(
        success=True,
        log="test_read_all_card")