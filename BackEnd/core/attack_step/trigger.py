from core.attack_step.attack_step_base import AttackStep
from core.attack_step.counter import Counter
from core.attack_type import AttackType
from core.data_reader import DataReader
from schemas import event_type,game_flow
from config import setting_ingame
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class Trigger(AttackStep):
    step_name="Trigger"
    next_step=Counter
    def __init__(self,attack_type:AttackType,stage_position_index:int):
        super().__init__(attack_type,True,stage_position_index)
        
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
        await self.trigger_check(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)
        
    async def trigger_check(self,game:"Game"):
        player_id=game.get_turn_player_id()
        card_id,trigger=game.player_check_trigger(player_id)
        triggers=[{"type":trigger}]
        player_name=game.get_turn_player_name()
        common=DataReader.get_common_data(
            game,True,
            f"{player_name}は{trigger}のトリガーをチェックしました",
            player_id)
        res=game_flow.AttackPhaseTriggerCheckResponse(
            common=common,
            trigger_card_id=card_id,
            triggers=triggers)
        await game.send_data_to_room(res)
        
        game.player_process_resolution_to_stock(player_id)