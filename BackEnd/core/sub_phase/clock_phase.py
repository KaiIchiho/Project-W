from core.sub_phase.phase_base import Phase
from core.sub_phase.main_phase import MainPhase
from schemas import event_type,game_flow
from core.data_reader import DataReader
from config import setting_ingame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class ClockPhase(Phase):
    phase_name="Clock Phase"
    next_phase=MainPhase
    def __init__(self):
        super().__init__()
        self.handlers[event_type.CLOCK_PHASE_CLOCK]="start_clock"
        
    async def on_enter(self, game):
        await super().on_enter(game)
    
    async def on_exit(self, game):
        await super().on_exit(game)
    
    async def start_clock(self,game:"Game",req:game_flow.ClockPhaseClockRequest,player_id:int):
        if not game.check_is_turn_player_command(player_id):
            return
        hand_index=req.clocked_hand_card.hand_index
        card_id=game.player_hand_to_clock(player_id,hand_index)
        success=False
        log=""
        player_name=game.get_player_name_by_id(player_id)
        if card_id!=-1:
            success=True
            log=f"{player_name}は1枚の手札をクロック置き場に置きました"
        else:
            log=f"{player_name}はクロック置き場に手札を置けませんでした"
        
        common=DataReader.get_common_data(game,success,log,player_id)
        res_self=game_flow.ClockPhaseClockSelfResponse(
            common=common,
            clocked_hand_card={"card_id":card_id})
        res_other=game_flow.ClockPhaseClockOtherResponse(
            common=common)
        await game.send_data_to_self_other(player_id,res_self,res_other)
        
        if success:
            await self.clock_draw(game,player_id)
    
    async def clock_draw(self,game:"Game",player_id:int):
        cards=[]
        success=True
        log=""
        for i in range(setting_ingame.CLOCK_DRAW):
            card_id=game.player_draw(player_id)
            if card_id==-1:
                success=False
            cards.append({"card_id":card_id})
        player_name=game.get_player_name_by_id(player_id)
        if success:
            log=f"{player_name}は山札から2枚のカードをドローしました"
        else:
            log=f"{player_name}は山札から2枚のカードをドローできませんでした"
        common=DataReader.get_common_data(
            game,success,log,player_id)
        res_self=game_flow.ClockPhaseDrowSelfResponse(
            common=common,add_two_hand_cards=cards
        )
        res_other=game_flow.ClockPhaseDrowOtherResponse(
            common=common
        )
        await game.send_data_to_self_other(player_id,res_self,res_other)