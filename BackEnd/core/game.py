from models.player import Player
#from BackEnd.core._attack_step import AttackStep
from typing import Callable,Optional,Awaitable
from core.sub_phase.phase_base import Phase
from core.sub_phase.standby_phase import StandbyPhase
#from core.attack_step.attack_step_base import AttackStep
from pydantic import BaseModel
from schemas import object,preparation,common
from schemas import game_flow

class Game():
    ws_send_message:Callable[[dict,str],Awaitable[None]]=None
    create_message:Callable[[int,str],dict]=None
    
    ws_send_data_to_user:Callable[[int,BaseModel],Awaitable[None]]
    ws_send_data_to_room:Callable[[int,BaseModel],Awaitable[None]]
    ws_send_data_to_room_except_target:Callable[[int,int,BaseModel],Awaitable[None]]
    
    phase:Optional[Phase]=None
    #attack_step:Optional[AttackStep]=None
    
    _is_in_progress=False
    
    def __init__(self,
                 room_id:int,
                 player_1:Optional[Player]=None,
                 player_2:Optional[Player]=None,
                 turn_player:Optional[Player]=None,
                 ):
        self.room_id=room_id
        
        if player_1 is not None and player_2 is not None and player_1 is player_2:
            raise ValueError("2 Player Are the Same")
        self.player_1=player_1
        self.player_2=player_2
        
        self.turn_player=turn_player
        self.current_turn=0
        #self.current_attack_step:AttackStep
        
        self.first_phase=StandbyPhase()
    
    async def _send_data_to_user(self,user_id:int,data:BaseModel):
        if self.ws_send_data_to_user:
            await self.ws_send_data_to_user(user_id,data)
    
    async def _send_data_to_room(self,room_id:int,data:BaseModel):
        if self.ws_send_data_to_room:
            await self.ws_send_data_to_room(room_id,data)
    
    async def _send_data_to_room_except_target(self,room_id:int,user_id:int,data:BaseModel):
        if self.ws_send_data_to_room_except_target:
            await self.ws_send_data_to_room_except_target(room_id,user_id,data)
    
    def set_player_1(self,player_1:Player):
        if player_1 is not None:
            if player_1 is self.player_2:
                raise ValueError("2 Player Are the Same.")
        self.player_1=player_1
    
    def set_player_2(self,player_2:Player):
        if player_2 is not None:
            if player_2 is self.player_1:
                raise ValueError("2 Player Are the Same.")
        self.player_2=player_2
    
    async def set_first_player(self,player:Player):
        if player is not self.player_1 and player is not self.player_2:
            raise ValueError("Player is not in Game.")
        self.turn_player=player
        
        # Send Data To Client
        await self._send_data_to_room(
            self.room_id,
            preparation.FirstTurnPlayerData(
                first_turn_player=player.player_id))
        
    async def set_player_to_none(
        self,player:Player,callback:Optional[Callable[[int],Awaitable[None]]]=None)->int:
        if player is None:
            raise ValueError("None Player !")
        elif player is self.player_1 or player is self.player_2:
            raise ValueError("2 Player Are the Same")
        
        if self.player_1 is None:
            self.player_1=player
            #if self.ws_send_message is not None:
            await self.send_message(
                "Standby Succeeded !",
                "Player 1 Standby",
                player.player_id)
            if callback is not None:
                await callback(player.player_id)
            return 1
        elif self.player_2 is None:
            self.player_2=player
            #if self.ws_send_message is not None:
            await self.send_message(
                "Standby Succeeded !",
                "Player 2 Standby",
                player.player_id)
            if callback is not None:
                await callback(player.player_id)
            return 2
        else:
            #if self.ws_send_message is not None:
            await self.send_message(
                "Standby Failed !",
                None,
                player.player_id)
            return -1
    
    async def cancel_set_player(self,player_id:int)->int:
        result=-1
        if self._is_in_progress:
            return result
        if self.player_1 and self.player_1.player_id==player_id:
            self.player_1=None
            result=1
        elif self.player_2 and self.player_2.player_id==player_id:
            self.player_2=None
            result=2
        return result
    
    def get_is_in_progress(self)->bool:
        return self._is_in_progress
    
    async def start_game(self,player_id:int):
        if self.check_is_full_players()==False:
            return
        self._is_in_progress=True
        # self.current_turn=1
        await self.set_first_player(self.player_1)
        await self.send_message(None,"Start Game",player_id)
        await self.__in_start_phase()
        
        log="ゲーム開始"
        common=self.get_common_data(
            "game_start",
            True,
            log,
            player_id)
        data=game_flow.StartGameResponse(
            common=common
        )
        await self.send_data_to_room(data)
    
    async def send_message(self,self_text:str,room_text:str,player_id:int):
        if self.create_message:
            message=self.create_message(self_text,room_text)
            await self.send_message_backage(message,player_id)
    
    async def send_message_backage(self,message:dict,player_id:int):
        if self.ws_send_message is not None:
            await self.ws_send_message(message,player_id)
    
    async def send_data_to_player(self,player_id:int,data:BaseModel):
        if self.ws_send_data_to_user:
            await self.ws_send_data_to_user(player_id,data)
    
    async def send_data_to_room(self,data:BaseModel):
        print("Log: send_data_to_room")
        if self.ws_send_data_to_room:
            await self.ws_send_data_to_room(self.room_id,data)
        else:
            print("Error: No ws_send_data_to_room")
    
    async def send_data_to_room_except_target(self,player_id:int,data:BaseModel):
        if self.ws_send_data_to_room_except_target:
            await self.ws_send_data_to_room_except_target(self.room_id,player_id,data)
    
    async def __in_start_phase(self):
        self.phase=self.first_phase
        await self.phase.on_enter(self)
    
    async def start_next_turn(self,player_switch:Callable[[],None]=None,in_start_phase:Callable[[],None]=None)->int:
        next_player=0
        if self.turn_player is self.player_1:
            self.turn_player=self.player_2
            next_player=2
        elif self.turn_player is self.player_2:
            self.turn_player=self.player_1
            next_player=1
        self.current_turn+=1
        await self.send_message(None,"Next Turn",self.turn_player.player_id)
        
        if player_switch is not None:
            player_switch()
        
        await self.__in_start_phase()
        if in_start_phase is not None:
            in_start_phase()
        
        return next_player
        
    async def handle_action(self,action:dict,player_id:int):
        if self.check_is_full_players()==False:
            await self.send_message("Game Is Not Players Full !",None,None)
            return
        
        await self.phase.handle_action(self,action,player_id)
        
        if self.phase.is_complete:
            await self.phase.on_next_phase(self,action)
    
    async def draw_initial_hand(self,player_id:int):
        player=self.check_command_player(player_id)
        success=True
        if not player:
            success=False
        for i in range(5):
            player.draw()
        common_data=self.get_common_data(
            "draw_initial_hand",
            success,
            self.turn_player.player_id,
            player.player_id)
        self.ws_send_data_to_room(self.room_id,common_data)
    
    def check_player_identity(self,user:Player)->int:
        if self.player_1 is user:
            return 1
        elif self.player_2 is user:
            return 2
        else:
            return -1
    
    def check_player_identity_by_id(self,player_id:int)->int:
        # player=None
        if self.player_1 and self.player_1.player_id==player_id:
            # player=self.player_1
            return 1
        elif self.player_2 and self.player_2.player_id==player_id:
            # player=self.player_2
            return 2
        else:
            return -1
        # player=self.check_command_player(player_id)
        # if player is None:
        #     print("Error: checked player is None")
        #     return -1
        # return self.check_player_identity(player)
    
    def check_turn_player_identity(self)->int:
        return self.check_player_identity(self.turn_player)
    
    def check_is_full_players(self)->bool:
        if self.player_1 is None or self.player_2 is None:
            return False
        else:
            return True
    
    def check_command_player(self,player_id:int)->Player:
        if self.player_1 is None or self.player_2 is None:
            return None
        print(f"player 1 ID: {self.player_1.player_id}")
        print(f"player 2 ID: {self.player_2.player_id}")
        print(f"checked player ID: {player_id}")
        if self.player_1.player_id==player_id:
            return self.player_1
        elif self.player_2.player_id==player_id:
            return self.player_2
        else:
            return None
        
    def check_is_turn_player_command(self,player_id:int)->bool:
        print(f"Check is Action Player ID: {player_id}")
        command_player=self.check_command_player(player_id)
        if command_player is None:
            print(f"Check is Action Player None")
            return False
        print(f"Command Player ID: {command_player.player_id}")
        print(f"Action Player ID: {self.turn_player.player_id}")
        if command_player is self.turn_player:
            print(f"Check is Action Player True")
            return True
        else:
            print(f"Check is Action Player False")
            return False
        
    async def forced_game_end(self):
        self._is_in_progress=False
        
        print("Log: forced game end.")
        if not self.ws_send_message:
            return
        
        player_id=""
        if self.player_1:
            player_id=self.player_1.player_id
        elif self.player_2:
            player_id=self.player_2.player_id
        
        if self.create_message:
            await self.ws_send_message(self.create_message(None,"Game End"),player_id)
            
    #-------------------------------------------
    def get_common_data(
        self,
        event:str,
        success:bool,
        log:str,
        event_user_id:int
    )->common.CommonData:
        player_1=self.get_player_data(self.player_1)
        player_2=self.get_player_data(self.player_2)
        turn_player_user_id=-1
        if self.turn_player:
            turn_player_user_id=self.turn_player.player_id
        return common.CommonData(
            event=event,
            success=success,
            log=log,
            turn_player_user_id=turn_player_user_id,
            event_user_id=event_user_id,
            player_1=player_1,
            player_2=player_2)
    
    def get_player_data(self,player:Player)->object.PlayerData:
        user_id=-1
        if player:
            user_id=player.player_id
        deck=self.get_deck_data(player)
        stage=self.get_stage_data(player)
        waiting_room=self.get_waiting_room_data(player)
        hand=self.get_hand_data(player)
        clock=self.get_clock_data(player)
        level=self.get_level_data(player)
        stock=self.get_stock_data(player)
        cx=self.get_cx_data(player)
        memory=self.get_memory_data(player)
        return object.build_object_data(
            "player",
            user_id=user_id,
            deck=deck,
            stage=stage,
            waiting_room=waiting_room,
            hand=hand,
            clock=clock,
            level=level,
            stock=stock,
            cx=cx,
            memory=memory)
    
    def get_deck_data(self,player:Player)->object.DeckData:
        # player=self.check_command_player(player_id)
        if not player:
            return object.DeckData()
        if not player.playmat:
            return object.DeckData()
        if not player.playmat.deck:
            return object.DeckData()
        cards:list[int]=[]
        for card in player.playmat.deck.cards:
            if card is None:
                continue
            cards.append(card.card_id)
        
        return object.build_object_data(
            "deck",
            card_num=len(cards),
            cards=cards)
    
    def get_stage_data(self,player:Player)->object.StageData:
        if not player:
            return object.StageData()
        if not player.playmat:
            return object.StageData()
        cards=[]
        for card in player.playmat.stage:
            if card is not None:
                cards.append(card.card_id)
        markers=[]
        for marker in player.playmat.markers:
            if marker is not None:
                markers.append(marker)
        return object.build_object_data(
            "stage",
            card_num=len(cards),
            cards=cards,
            markers=markers
        )
    
    def get_waiting_room_data(self,player:Player)->object.WaitingRoomData:
        # player=self.check_command_player(player_id)
        if not player:
            return object.WaitingRoomData()
        if not player.playmat:
            return object.WaitingRoomData()
        cards:list[int]=[]
        for card in player.playmat.waiting_room:
            if card is None:
                continue
            cards.append(card.card_id)
        
        return object.build_object_data(
            "waiting_room",
            card_num=len(cards),
            cards=cards)
    
    def get_hand_data(self,player:Player)->object.HandData:
        # player=self.check_command_player(player_id)
        if not player:
            return object.HandData()
        cards:list[int]=[]
        for card in player.hand:
            if card is None:
                continue
            cards.append(card.card_id)
        
        return object.build_object_data(
            "hand",
            card_num=len(cards),
            cards=cards)

    
    def get_clock_data(self,player:Player)->object.ClockData:
        # player=self.check_command_player(player_id)
        if not player:
            return object.ClockData()
        if not player.playmat:
            return object.ClockData()
        cards:list[int]=[]
        for card in player.playmat.clock:
            if card is None:
                continue
            cards.append(card.card_id)
        
        return object.build_object_data(
            "clock",
            card_num=len(cards),
            cards=cards)
    
    def get_level_data(self,player:Player)->object.LevelData:
        # player=self.check_command_player(player_id)
        if not player:
            return object.LevelData()
        if not player.playmat:
            return object.LevelData()
        cards:list[int]=[]
        for card in player.playmat.level:
            if card is None:
                continue
            cards.append(card.card_id)
        
        return object.build_object_data(
            "level",
            card_num=len(cards),
            cards=cards)
    
    def get_stock_data(self,player:Player)->object.StockData:
        # player=self.check_command_player(player_id)
        if not player:
            return object.StockData()
        if not player.playmat:
            return object.StockData()
        cards:list[int]=[]
        for card in player.playmat.stock:
            if card is None:
                continue
            cards.append(card.card_id)
        
        return object.build_object_data(
            "stock",
            card_num=len(cards),
            cards=cards)
    
    def get_cx_data(self,player:Player)->object.CXData:
        # player=self.check_command_player(player_id)
        if not player:
            return object.CXData()
        if not player.playmat:
            return object.CXData()
        card_id:int=-1
        if player.playmat.climax:
            card_id=player.playmat.climax.card_id
        
        return object.build_object_data(
            "cx",
            card_id=card_id)
    
    def get_memory_data(self,player:Player)->object.MemoryData:
        # player=self.check_command_player(player_id)
        if not player:
            return object.MemoryData()
        if not player.playmat:
            return object.MemoryData()
        cards:list[int]=[]
        for card in player.playmat.memory:
            if card is None:
                continue
            cards.append(card.card_id)
        
        return object.build_object_data(
            "memory",
            card_num=len(cards),
            cards=cards)