from core.state_machine_base import StateMachine
from schemas import event_type,game_flow
from core.data_reader import DataReader
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game

class Phase(StateMachine):
    _is_frozen:bool=False
    handlers={
        event_type.NEXT_PHASE:"on_next_phase",
        event_type.NEXT_TURN:"on_next_turn",
        event_type.LEVEL_UP:"process_level_up"
    }
    is_complete=False
    phase_name="phase_base"
    next_phase=None
    def __init_subclass__(cls, **kwargs):
        super.__init_subclass__(**kwargs)
        cls.handlers=cls.handlers.copy()
    
    def is_frozen(self)->bool:
        return self._is_frozen
    
    async def on_enter(self,game:"Game"):
        print(f"Log: {self.phase_name} On Enter")
        common=DataReader.get_common_data(
            game,True,
            f"{self.phase_name}が始まります",
            game.get_turn_player_id())
        res=game_flow.OnPhaseChangedResponse(
            common=common)
        await game.send_data_to_room(res)
    async def on_exit(self,game:"Game"):
        print(f"Log: {self.phase_name} On Exit")
        
    async def on_next_phase(self,game:"Game",req:game_flow.NextPhaseRequest,player_id:int):
        print("Log: on_next_phase")
        if not game.check_is_turn_player_command(player_id):
            return
        await game.transition_to_next_phase(player_id,self._end_next_phase)        
    
    async def _end_next_phase(self,game:"Game",player_id:int,is_next_phase:bool):
        log=""
        if not is_next_phase:
            print("Log: on_next_phase, Next Phase Is None")
            log="まもなく、次のターンを始めます"
        else:
            print("Log: on_next_phase, Next Phase Is Not None")
            log=f"{game.get_player_name_by_id(player_id)}の{game.phase.next_phase.phase_name}フェーズに遷移します"
        
        common=DataReader.get_common_data(
            game,True,log,player_id)
        res=game_flow.NextPhaseResponse(common=common)
        await game.send_data_to_room(res)
        
        if not is_next_phase:
            if not game.check_is_first_phase():
                await self.on_next_turn(game,None,player_id)
            else:
                await self.on_next_turn(game,None,player_id,False)
    
    async def on_next_turn(self,game:"Game",req:game_flow.NextTurnRequest,player_id:int,is_switch_turn_player:bool=True):
        if not game.check_is_turn_player_command(player_id):
            return
        
        await game.start_next_turn(
            player_id,
            is_switch_turn_player,
            self.on_turn_switched)
        
    async def on_turn_switched(self,game:"Game",player_id:int):
        common=DataReader.get_common_data(
            game,True,
            f"次の{game.get_turn_player_name()}のターンが始まります",
            player_id)
        res=game_flow.NextTurnResponse(common=common)
        await game.send_data_to_room(res)
    
    async def send_message_list(self,game:"Game",message_list:list[dict],default_player_id:int):
        for message in message_list:
            room_message_text=""
            player_id=message.get("player_id")
            if player_id is None:
                player_id=default_player_id
            identity=game.check_player_identity_by_id(player_id)
            if identity!=-1:
                room_message_text=f"Player {identity}'s Action: "
                
            if message.get("room") is not None:
                message["room"]=room_message_text+message["room"]
            await game.send_message_backage(message,player_id)
    
    async def start_level_up(self,game:"Game",player_id:int):
        player_name=game.get_player_name_by_id(player_id)
        common=DataReader.get_common_data(
            game,True,
            f"{player_name}はレベルアップが発生しました",
            player_id)
        res=game_flow.LevelUpResponse(common=common)
        self.set_waiting_event(common.event,player_id)
        await game.send_data_to_room(res)
        
    async def process_level_up(
        self,game:"Game",
        req:game_flow.LevelUpRequest,
        player_id:int
    ):
        print("Log: process_level_up")
        success=\
            game.player_process_level_up(
                player_id,req.chosen_clock_card)
        player_name=game.get_player_name_by_id(player_id)
        if success:
            # log=f"{player_name}のレベルアップが処理されました"
            log=f"{player_name} Process Level Up Successed"
        else:
            # log=f"{player_name}のレベルアップが処理失敗です"
            log=f"{player_name} Process Level Up Failed"
        print(log)