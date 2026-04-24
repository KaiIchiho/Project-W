from core.attack_step.attack_step_base import AttackStep
from core.attack_step.battle import Battle
from core.attack_type import AttackType
from core.data_reader import DataReader
from schemas import event_type,game_flow
from typing import TYPE_CHECKING,Callable
if TYPE_CHECKING:
    from core.game import Game

class Damage(AttackStep):
    step_name="Damage"
    next_step=Battle
    def __init__(self,auto_next_step:Callable[[],None],attack_type:AttackType,stage_position_index:int):
        super().__init__(auto_next_step,attack_type,True,stage_position_index)
        
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
        await self.player_damage_check(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)
        
    async def player_damage_check(self,game:"Game"):
        player_id=game.get_turn_player_id()
        info_type=["card_soul"]
        info_dict=game.get_player_stage_info(info_type)
        soul=info_dict.get("card_soul")
        master_user_id=\
            game.get_player_stage_owner_id(player_id,self.stage_position_index)
        attack_character={
                "index":self.stage_position_index,
                "master_user_id":master_user_id,
                "soul":soul
            }
        if master_user_id==-1:
            success=False
            log="ダメージがチェックされました"
        else:
            success=True
            log="ダメージのチェックが失敗しました"
        
        common=DataReader.get_common_data(
            game,success,log,player_id
        )
        res=game_flow.AttackPhaseDamageCheckResponse(
            common=common,
            attack_character=attack_character
        )
        await game.send_data_to_room(res)
        
        self.is_complete=True