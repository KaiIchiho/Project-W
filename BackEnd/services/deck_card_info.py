from schemas.deck_card_info import ReadDeckRequest,ReadDeckResponse
from db import deck_repo

def read_deck(req:ReadDeckRequest)->ReadDeckResponse:
    deck_repo.test_read_all_deck()
    return ReadDeckResponse(
        success=True,
        log="test_read_all_deck")