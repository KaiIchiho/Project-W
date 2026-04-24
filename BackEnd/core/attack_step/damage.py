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
        player_name=game.get_turn_player_name()
        has_card=game.player_has_stage_card(player_id,self.stage_position_index)
        if has_card:
            info_type=["card_soul"]
            info_dict=game.get_player_stage_info(
                player_id,self.stage_position_index,info_type)
            soul=info_dict.get("card_soul")
            master_user_id=\
                game.get_player_stage_owner_id(
                    player_id,self.stage_position_index)
            attack_character={
                    "index":self.stage_position_index,
                    "master_user_id":master_user_id,
                    "soul":soul
                }
            if master_user_id!=-1:
                success=True
                log=f"{player_name}はダメージがチェックされました"
            else:
                success=False
                log=f"{player_name}はダメージのチェックが失敗しました"
        else:
            success=False
            log="攻撃したカード存在しないので、ダメージ処理はしません"
            attack_character={
                "index":self.stage_position_index,
                "master_user_id":-1,
                "soul":-1
            }
        
        common=DataReader.get_common_data(
            game,success,log,player_id)
        res=game_flow.AttackPhaseDamageCheckResponse(
            common=common,
            attack_character=attack_character)
        await game.send_data_to_room(res)
        
        self.is_complete=True