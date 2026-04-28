from core.attack_step.attack_step_base import AttackStep
from core.data_reader import DataReader
from schemas import event_type,game_flow
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class Encore(AttackStep):
    step_name="Encore"
    def __init__(self):
        super().__init__(None,None,True)
        self.handlers[event_type.ATTACK_PHASE_ENCORE]="on_encore"
        self.waiting_process_stage:dict={}
        self.process_player_order:list[int]=[]
        self.processing_player_id:int=-1
    
    async def on_enter(self,game:"Game"):
        await super().on_enter(game)
        self._init_reverse_list_for_waiting_process(game)
        await self.start_encore_check(game)
    
    async def on_exit(self,game:"Game"):
        await super().on_exit(game)
    
    def _init_reverse_list_for_waiting_process(self,game:"Game"):
        player_id=game.get_turn_player_id()
        other_player_id=game.get_other_player_id()
        self.waiting_process_stage[player_id]=game.get_player_stage_reverse_index(player_id)
        self.waiting_process_stage[other_player_id]=game.get_player_stage_reverse_index(other_player_id)
        self.process_player_order.append(player_id)
        self.process_player_order.append(other_player_id)
        print(f"Log: Initialized waiting_process_stage: {self.waiting_process_stage}")
    
    async def start_encore_check(self,game:"Game"):
        if not self.process_player_order:
            await self.end_encord_check(game)
            return
        
        self.processing_player_id=\
            self.process_player_order.pop(0)
            
        await self.request_player_encore_check(game,self.processing_player_id)
    
    async def request_player_encore_check(self,game:"Game",player_id:int):
        player_name=game.get_player_name_by_id(player_id)
        self_processing_stage_list=\
            self.waiting_process_stage.get(player_id)
        
        if self_processing_stage_list is not None:
            reverse_card_on_stage=[]
            for stage in self_processing_stage_list:
                reverse_card_on_stage.append({"stage_position":stage})
            
        common=DataReader.get_common_data(
            game,True,
            f"{player_name}はアンコールを行います",
            player_id)
        res=game_flow.AttackPhaseEncoreResponse(
            common=common,
            reverse_card_on_stage=reverse_card_on_stage
        )
        await game.send_data_to_room(res)
    
    async def end_encord_check(self,game:"Game"):
        await self.on_next_step(game)
    
    async def on_encore(
        self,game:"Game",
        req:game_flow.AttackPhaseEncoreRequest,
        player_id:int
    ):
        if player_id!=self.processing_player_id:
            return
        
        for index in req.order:
            game.remove_stage_char_to_waiting_room(player_id,index)
        
        # アンコール能力の処理
        
        await self.start_encore_check(game)