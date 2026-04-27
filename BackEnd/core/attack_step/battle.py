from core.attack_step.attack_step_base import AttackStep
from core.attack_type import AttackType
from core.data_reader import DataReader
from schemas import event_type,game_flow
from models.playmat import StageStatus
from typing import TYPE_CHECKING,Callable
if TYPE_CHECKING:
    from core.game import Game

class Battle(AttackStep):
    step_name="Battle"
    next_step=None
    def __init__(self,auto_next_step:Callable[[],None],attack_type:AttackType,stage_position_index:int):
        super().__init__(auto_next_step,attack_type,True,stage_position_index)
        
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
        await self.on_battle(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)
        
    async def on_battle(self,game:"Game"):
        player_id=game.get_turn_player_id()
        player_name=game.get_turn_player_name()
        other_player_id=game.get_other_player_id()
        
        master_user_id=game.get_player_stage_owner_id(
            player_id,self.stage_position_index)
        power=game.get_player_stage_info(
            player_id,
            self.stage_position_index,
            ["card_power"])\
                .get("card_power")
        status=game.get_player_stage_status(
            player_id,self.stage_position_index)
        status_value=status.value if status is not None else None
        
        other_stage_index=game.get_other_stage_index(
            self.stage_position_index)
        other_master_user_id=game.get_player_stage_owner_id(
            other_player_id,other_stage_index)
        other_power=game.get_player_stage_info(
            other_player_id,
            other_stage_index,
            ["card_power"])\
                .get("card_power")
        other_status=game.get_player_stage_status(other_player_id,other_stage_index)
        other_status_value=other_status.value\
            if other_status is not None else None
        
        common=DataReader.get_common_data(
            game,True,
            f"{player_name}はバトルを行います",
            player_id
        )
        attack_character={
            "stage_position_index":self.stage_position_index,
            "master_user_id":master_user_id,
            "power":power,
            "card_status":status_value
        }
        defense_character={
            "stage_position_index":self.stage_position_index,
            "master_user_id":other_master_user_id,
            "power":other_power,
            "card_status":other_status_value
        }
        res=game_flow.AttackPhaseBattleProcessResponse(
            common=common,
            attack_character=attack_character,
            defense_character=defense_character
        )
        await game.send_data_to_room(res)
        
        await self.on_next_step(game)