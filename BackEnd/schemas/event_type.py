from schemas import game_flow

ENTER_ROOM="enter_room"
EXIT_ROOM="exit_room"
SELECT_DECK="select_deck"
STANDBY="standby"
GAME_START="game_start"
FIRST_TURNPLAYER="first_turnplayer"
DRAW_INITIAL_HAND="draw_initial_hand"
SWAP_HAND_CARDS="swap_hand_cards"

NEXT_PHASE="next_phase"
NEXT_TURN="next_turn"

event_req={
    SWAP_HAND_CARDS:game_flow.SwapHandCardsRequest
}