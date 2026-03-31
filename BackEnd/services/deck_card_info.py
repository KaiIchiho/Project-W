from schemas.deck_card_info import DeckInfo,DeckListRequest,DeckListResponse
from db import deck_repo

def deck_list(req:DeckListRequest)->DeckListResponse:
    deck_list=deck_repo.read_all_deck()
    deck_info_list=[]
    for deck in deck_list:
        deck_id=deck.get("deck_id")
        deck_name=deck.get("deck_name")
        if deck_id is None:
            deck_id=-1
        if deck_name is None:
            deck_name=""
        deck_info=DeckInfo(deck_id=deck_id,deck_name=deck_name)
        deck_info_list.append(deck_info)
    return DeckListResponse(deck_list=deck_info_list)