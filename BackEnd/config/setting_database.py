#HOST='127.0.0.1'
HOST="wssim-db.c76cg4ksyw72.ap-northeast-1.rds.amazonaws.com"
PORT=3306
USER='wssim_admin'
PASSWORD='wssim_sim_db'
DATABASE='wssimdb'

USER_TABLE='tbl_users'
ROOM_TABLE='tbl_rooms'
DECK_TABLE='tbl_decks'
DECK_CARDS_TABLE='tbl_deck_cards'
CARD_TABLE='tbl_cards'
ALLOWED_TABLES={
    USER_TABLE,
    ROOM_TABLE,
    DECK_TABLE,
    DECK_CARDS_TABLE,
    CARD_TABLE
}

POOL_SIZE=5