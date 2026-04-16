from schemas.deck_card_info import DeckInfo,DeckListRequest,DeckListResponse,CardInfoRequest,CardInfoResponse
from db import deck_repo,card_repo

def deck_list(req:DeckListRequest)->DeckListResponse:
    deck_list=deck_repo.read_all_deck()
    deck_info_list=[]
    for deck in deck_list:
        print(deck)
        deck_id=deck.get("id")
        deck_name=deck.get("name")
        if deck_id is None:
            deck_id=-1
        if deck_name is None:
            deck_name=""
        deck_info=DeckInfo(deck_id=deck_id,deck_name=deck_name)
        deck_info_list.append(deck_info)
    return DeckListResponse(deck_list=deck_info_list)

def card_info(req:CardInfoRequest)->CardInfoResponse:
    result=card_repo.read_card_field_list(req.card_id,req.columns)
    res=CardInfoResponse(
        success=True,
        columns=result,
        log="カード情報の取得が成功しました")
    return res
    