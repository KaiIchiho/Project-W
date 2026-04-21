from core.sub_phase.phase_base import Phase
from core.data_reader import DataReader
from schemas import event_type,game_flow
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class EndPhase(Phase):
    phase_name="End Phase"
    next_phase=None
    def __init__(self):
        super().__init__()
        self.handlers[event_type.END_PHASE_HAND_DISCARD]="discard_turn_player_hand"
        
    async def on_enter(self, game):
        await super().on_enter(game)
        await self.remove_turn_player_cx(game)
        await self.check_turn_player_hand_with_limit()
    
    async def on_exit(self, game):
        await super().on_exit(game)
    
    async def remove_turn_player_cx(self,game:"Game"):
        has_set_cx=game.remove_cx_card(game.get_turn_player_id())
        player_name=game.get_turn_player_name()
        common=DataReader.get_common_data(
            game,True,
            f"{player_name}のCXカードがCX置き場から控え室に移動しました",
            game.get_turn_player_id())
        res=game_flow.EndPhaseCXRemoveResponse(
            common=common,is_cx_zone_empty=not has_set_cx)
        await game.send_data_to_room(res)
    
    async def check_turn_player_hand_with_limit(self,game:"Game"):
        player_name=game.get_turn_player_name()
        player_id=game.get_turn_player_id()
        exceed=game.get_hand_exceed_limit(player_id)
        if exceed>0:
            common_self=DataReader.get_common_data(
                game,True,
                f"{player_name}の手札の枚数は上限を{exceed}枚超えたので、超えた枚数のカードを捨ててください",
                player_id)
            res_self=game_flow.EndPhaseHandExceedResponse(
                common=common_self,exceed_hand_card_num=exceed)
            
            common_other=DataReader.get_common_data(
                game,True,
                f"{player_name}は上限超えた手札を処理しています",
                player_id)
            res_other=game_flow.EndPhaseHandExceedResponse(
                common=common_other,exceed_hand_card_num=exceed)
            await game.send_data_to_self_other(
                player_id,res_self,res_other)
            
    async def discard_turn_player_hand(
        self,
        game:"Game",
        req:game_flow.EndPhaseHandDiscardRequest,
        player_id:int
    ):
        if not game.check_is_turn_player_command(player_id):
            return
        hand_index_list=req.set_waiting_room
        success=False
        log=""
        player_name=game.get_player_name_by_id(player_id)
        if len(hand_index_list)!=game.get_hand_exceed_limit(player_id):
            log=f"{player_name}は捨てたい手札の数が誤っています"
        else:
            success=game.discard_hand_by_list(player_id,hand_index_list)
            if success:
                log=f"{player_name}は手札の枚数を上限以下になるようにカードを控え室に置きました"
            else:
                log=f"{player_name}は手札の枚数を上限以下になるようにカードを控え室に置けませんでした"
            
        common=DataReader.get_common_data(
            game,success,log,player_id)
        res=game_flow.EndPhaseHandDiscardResponse(
            common=common,throw_hand_card=hand_index_list)
        await game.send_data_to_room(res)