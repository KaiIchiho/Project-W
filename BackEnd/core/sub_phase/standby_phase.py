from core.sub_phase.phase_base import Phase
from schemas import event_type,game_flow
from core.data_reader import DataReader
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
        game.init_players_playmat()
        await self.all_players_deck_shuffle(game)
        await self.draw_players_initial_hand(game)
    
    async def all_players_deck_shuffle(self,game:"Game"):
        if not game.check_is_full_players():
            return
        await self.player_deck_shuffle(game,game.get_turn_player_id())
        await self.player_deck_shuffle(game,game.get_other_player_id())
    
    async def player_deck_shuffle(self,game:"Game",player_id:int):
        result=False
        log=""
        player_identity=game.check_player_identity_by_id(player_id)
        if player_identity==-1:
            log=f"{player_id}のプレイヤーはゲーム内に存在しません"
        else:
            result=game.player_deck_shuffle(player_id)
            player_name=game.get_player_name_by_id(player_id)    
            if result:
                log=f"{player_name}のシャッフルが成功しました"
            else:
                log=f"{player_name}のシャッフルが失敗しました"
        
        common=DataReader.get_common_data(
            game,result,log,player_id)
        res=game_flow.ShuffleResponse(common=common)
        await game.send_data_to_room(res)
    
    async def draw_players_initial_hand(self,game:"Game"):
        result=False
        log="" 
        result_1=game.draw_initial_hand(game.get_turn_player_id())
        result_2=game.draw_initial_hand(game.get_other_player_id())
        if result_1 and result_2:
            result=True
            log="初期手札のドロー（各5枚）が成功しました"
        else:
            log="初期手札のドローが失敗しました"
        
        common=DataReader.get_common_data(
            game,result,log,-1)
        res=game_flow.DrawInitialHandResponse(
            common=common)
        await game.send_data_to_room(res)
    
    async def on_swap_hand_cards(
        self,game:"Game",req:game_flow.SwapHandCardsRequest,player_id:int
    ):
        hand_index_list=req.hand_index
        success,identity=await game.swap_hand_cards(player_id,hand_index_list)
        log=""
        if success:
            log=f"{game.get_player_name_by_id(player_id)}は手札の入れ替えが成功しました"
        else:
            if identity==2:
                log="先攻プレイヤーはまだ手札の入れ替えが完成していません"
            elif identity==-1:
                log=f"{player_id}のプレイヤーはゲーム内に存在しません"
            else:
                log=f"{game.get_player_name_by_id(player_id)}は手札の入れ替えが失敗しました"
        
        common=DataReader.get_common_data(
            game,success,log,player_id)
        res=game_flow.SwapHandCardsResponse(
            common=common)
        await game.send_data_to_room(res)
        
        if success and identity==2:
            await self.on_next_phase(game,None,game.get_turn_player_id())
        