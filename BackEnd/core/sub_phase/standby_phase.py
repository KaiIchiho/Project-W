from core.sub_phase.phase_base import Phase
from schemas import event_type,game_flow
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class StandbyPhase(Phase):
    phase_name="Standby Phase"
    next_phase=None
    def __init__(self):
        super().__init__()
        self.handlers={
            event_type.SWAP_HAND_CARDS:"on_swap_hand_cards"
        }
        
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
        # self.init_playmat(game)
        game.init_players_playmat()
        await game.all_players_deck_shuffle()
        # await self.draw_initial_hand(game)
        await game.draw_players_initial_hand()
    
    # def init_playmat(self,game:"Game"):
    #     result_1,result_2=game.init_players_playmat()
    #     print("Log: init_playmat")
    #     print("Log: player 1 Init Playmat: ",result_1)
    #     print("Log: player 2 Init Playmat: ",result_2)
        
    # async def draw_initial_hand(self,game:"Game"):
        # print("Log: StandbyPhase draw_initial_hand")
        # await game.draw_players_initial_hand()
        # print("Log: draw_players_initial_hand ",result)
    
    async def on_swap_hand_cards(
        self,game:"Game",req:game_flow.SwapHandCardsRequest,player_id:int
    ):
        hand_index_list=req.hand_index
        await game.swap_hand_cards(player_id,hand_index_list)