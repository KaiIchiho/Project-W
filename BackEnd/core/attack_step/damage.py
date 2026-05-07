from core.attack_step.attack_step_base import AttackStep
from core.attack_step.battle import Battle
from core.attack_type import AttackType
from core.data_reader import DataReader
from schemas import event_type,game_flow
from typing import TYPE_CHECKING,Callable,Awaitable
if TYPE_CHECKING:
    from core.game import Game

class Damage(AttackStep):
    step_name="Damage"
    next_step=Battle
    has_attack_card:bool=True
    attack_card_soul:int=-1
    def __init__(self,auto_next_step:Callable[["Game"],Awaitable[None]],attack_type:AttackType,stage_position_index:int):
        super().__init__(auto_next_step,attack_type,True,stage_position_index)
        
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
        await self.player_damage_check(game)
        await self.player_damage_process(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)
        
    async def player_damage_check(self,game:"Game"):
        player_id=game.get_turn_player_id()
        player_name=game.get_other_player_name()
        self.has_attack_card=game.player_has_stage_card(player_id,self.stage_position_index)
        if self.has_attack_card:
            info_type=["card_soul"]
            info_dict=game.get_player_stage_info(
                player_id,self.stage_position_index,info_type)
            self.attack_card_soul=info_dict.get("card_soul")
            master_user_id=\
                game.get_player_stage_owner_id(
                    player_id,self.stage_position_index)
            attack_character={
                "index":self.stage_position_index,
                "master_user_id":master_user_id,
                "soul":self.attack_card_soul
            }
            if master_user_id!=-1:
                success=True
                log=f"{player_name}はダメージがチェックされました"
            else:
                success=False
                log=f"{player_name}はダメージのチェックが失敗しました"
        else:
            success=False
            log="攻撃したカード存在しないため、ダメージ処理はしません"
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
        
    async def player_damage_process(self,game:"Game"):
        if not self.has_attack_card:
            return
        player_id=game.get_turn_player_id()
        player_name=game.get_turn_player_name()
        other_player_id=game.get_other_player_id()
        revealed_card_info=["card_type"]
        
        soul_damage=self._calculate_damage(game,player_id)
        
        is_broken,revealed_card=\
            game.player_check_damage(
                other_player_id,
                soul_damage,
                revealed_card_info)
        
        common=DataReader.get_common_data(
            game,True,
            f"{player_name}はダメージ処理を行います",
            player_id)
        res=game_flow.AttackPhaseDamageProcessResponse(
            common=common,
            revealed_card=revealed_card,
            is_damage_cancel=is_broken)
        await game.send_data_to_room(res)
        
        if is_broken:
            print(f"{player_id} process resolution to waiting room")
            # game.player_process_resolution_to_waiting_room(player_id)
            await game.player_start_handle_resolution(player_id,"waiting_room")
        else:
            print(f"{player_id} process resolution to clock")
            # await game.player_process_resolution_to_clock(player_id)
            await game.player_start_handle_resolution(player_id,"clock")
            
        await self.on_next_step(game)
        
    def _calculate_damage(self,game:"Game",player_id:int)->int:
        if self.attack_type==AttackType.DIRECT:
            soul_damage=self.attack_card_soul+1
        elif self.attack_type==AttackType.FRONT:
            soul_damage=self.attack_card_soul
        elif self.attack_type==AttackType.SIDE:
            other_stage_index,is_empty,info_dict=\
                game.get_other_player_stage_info(
                    player_id,
                    self.stage_position_index,
                    ["card_level"])
            other_level=info_dict.get("card_level")
            soul_damage=self.attack_card_soul-other_level
        if soul_damage<0:
            soul_damage=0
            
        return soul_damage