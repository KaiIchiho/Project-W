from models.player import Player
from typing import Callable,Optional,Awaitable
from core.sub_phase.phase_base import Phase
from core.sub_phase.standby_phase import StandbyPhase
from core.sub_phase.stand_phase import StandPhase
from pydantic import BaseModel
from schemas import object,common,game_flow

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
        
        self.first_phase=StandbyPhase
        self.pre_turn_first_phase=StandPhase
    
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
        
        common=self.get_common_data(
            # "first_turnplayer",
            True,
            f"先攻プレイヤーは{player.name}",
            player.player_id
        )
        
        # Send Data To Client
        await self._send_data_to_room(
            self.room_id,
            game_flow.FirstTurnPlayerResponse(
                common=common,
                first_turn_player=player.player_id))
        
    async def set_player_to_none(
        self,player:Player
        # ,callback:Optional[Callable[[int],Awaitable[None]]]=None
    )->int:
        if player is None:
            raise ValueError("None Player !")
        elif player is self.player_1 or player is self.player_2:
            raise ValueError("2 Player Are the Same")
        
        result=-1
        if not player.check_has_deck():
            return result
        
        if self.player_1 is None:
            self.player_1=player
            result=1
        elif self.player_2 is None:
            self.player_2=player
            result=2
        
        return result
    
    def cancel_set_player(self,player_id:int)->int:
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
        # await self.send_message(None,"Start Game",player_id)
        
        log="ゲーム開始"
        common=self.get_common_data(
            True,
            log,
            player_id)
        data=game_flow.GameStartResponse(
            common=common
        )
        await self.send_data_to_room(data)
        
        await self._in_start_phase()
    
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
    
    async def _in_start_phase(self):
        self.phase=self.first_phase()
        await self.phase.on_enter(self)
    
    async def _in_turn_start_phase(self):
        self.phase=self.pre_turn_first_phase()
        await self.phase.on_enter(self)
    
    async def start_next_turn(
        self,
        player_id:int,
        is_switch_turn_player:bool=True,
        on_player_switch:Callable[[],None]=None,
        in_turn_start_phase:Callable[[],None]=None
    )->int:
        print("Log: start_next_turn")
        if is_switch_turn_player:
            if self.turn_player is self.player_1:
                self.turn_player=self.player_2
            elif self.turn_player is self.player_2:
                self.turn_player=self.player_1
        self.current_turn+=1
        # await self.send_message(None,"Next Turn",self.turn_player.player_id)
        
        if on_player_switch is not None:
            on_player_switch()
        await self._in_turn_start_phase()
        if in_turn_start_phase is not None:
            in_turn_start_phase()
        
        common=self.get_common_data(
            True,f"次の{self.turn_player.name}のターンが始まります",player_id)
        res=game_flow.NextTurnResponse(common=common)
        await self.send_data_to_room(res)
        
    def init_players_playmat(self)->bool:
        if not self.check_is_full_players():
            return False
        result_1=self.player_1.init_playmat()
        result_2=self.player_2.init_playmat()
        return result_1,result_2
    
    async def all_players_deck_shuffle(self):
        if not self.check_is_full_players():
            return
        print("Log: all_players_deck_shuffle Start")
        await self.player_deck_shuffle(self.player_1.player_id)
        await self.player_deck_shuffle(self.player_2.player_id)
        print("Log: all_players_deck_shuffle End")
    
    async def player_deck_shuffle(self,player_id:int):
        player_identity=self.check_player_identity_by_id(player_id)
        result=False
        log=""
        player=None
        if player_identity==1 and self.player_1:
            player=self.player_1
        elif player_identity==2 and self.player_2:
            player=self.player_2
        
        if player:
            result=player.deck_shuffle()
            if result:
                log=f"{player.name}のシャッフルが成功しました"
            else:
                log=f"{player.name}のシャッフルが失敗しました"
        else:
            log=f"{player_id}のプレイヤーはゲーム内に存在しません"
        
        print(log)
        common=self.get_common_data(result,log,player_id)
        res=game_flow.ShuffleResponse(common=common)
        await self.send_data_to_room(res)
    
    async def handle_action(self,action:dict,event:str,player_id:int):
        if self.check_is_full_players()==False:
            await self.send_message("Game Is Not Players Full !",None,None)
            return
        
        await self.phase.handle_action(self,action,event,player_id)
        
        if self.phase.is_complete:
            await self.phase.on_next_phase(self,action)
    
    async def draw_players_initial_hand(self)->bool:
        result=False
        log=""
        if self.check_is_full_players():    
            result_1=await self.draw_initial_hand(self.player_1)
            result_2=await self.draw_initial_hand(self.player_2)
            if result_1 and result_2:
                result=True
                log="初期手札のドロー（各5枚）が成功しました"
            elif not result_1:
                log=f"{self.player_1.name}の初期手札のドローが失敗しました"
            elif not result_2:
                log=f"{self.player_2.name}の初期手札のドローが失敗しました"
            
        
        common=self.get_common_data(result,log,-1)
        res=game_flow.DrawInitialHandResponse(
            common=common
        )
        await self.send_data_to_room(res)
    
    async def draw_initial_hand(self,player:Player)->bool:
        if self.check_player_identity(player)==-1:
            return False
        for i in range(5):
            player.draw()
        return True
    
    async def swap_hand_cards(self,player_id:int,hand_index_list:list[int]):
        success=False
        log=""
        player:Player=self.check_command_player(player_id)
        identity=self.check_player_identity(player)
        if player:
            if identity==2 and not self.player_1.get_is_swap_hand():
                log="先攻プレイヤーはまだ手札の入れ替えが完成していません"
            else:
                success=player.swap_hand_cards(hand_index_list)
                if success:
                    log=f"{player.name}は手札の入れ替えが成功しました"
                else:
                    log=f"{player.name}は手札の入れ替えが失敗しました"
        else:
            log=f"{player_id}のプレイヤーはゲーム内に存在しません"
        
        common=self.get_common_data(success,log,player_id)
        res=game_flow.SwapHandCardsResponse(
            common=common
        )
        await self.send_data_to_room(res)
        
        if identity==2 and success:
            await self._end_start_phase()
        
    async def _end_start_phase(self):
        print("Log: _end_start_phase")
        if isinstance(self.phase,self.first_phase):
            await self.transition_to_next_phase(self.turn_player.player_id)
    
    async def transition_to_next_phase(self,player_id:int):
        log=""
        print(f"Log: on_next_phase, Now Phase Is {self.phase.phase_name}")
        await self.phase.on_exit(self)
        _is_next_phase=False
        if self.phase.next_phase is None:
            _is_next_phase=False
            print("Log: on_next_phase, Next Phase Is None")
            log="まもなく、次のターンを始めます"
        else:
            _is_next_phase=True
            print("Log: on_next_phase, Next Phase Is Not None")
            log=f"{self.turn_player.name}の{self.phase.next_phase.phase_name}フェーズに遷移します"
        
        common=self.get_common_data(
            True,
            log,
            player_id)
        res=game_flow.NextPhaseResponse(common=common)
        await self.send_data_to_room(res)
        
        if not _is_next_phase:
            if not isinstance(self.phase,self.first_phase):
                await self.start_next_turn(player_id)
            else:
                await self.start_next_turn(player_id,False)
        else:
            self.phase=self.phase.next_phase()
            await self.phase.on_enter(self)
    
    async def phase_enter_response(self):
        common=self.get_common_data(
            True,
            f"{self.phase.phase_name}が始まります",
            self.turn_player.player_id
        )
        res=game_flow.OnPhaseChangedResponse(
            common=common
        )
        await self.send_data_to_room(res)
        
    async def phase_exit_response(self):
        pass
        # common=self.get_common_data(
        #     True,
        #     f"{self.phase.phase_name}が始まります",
        #     self.turn_player.player_id
        # )
        # res=game_flow.OnPhaseChangedResponse(
        #     common=common
        # )
        # await self.send_data_to_room(res)
            
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
            return 1
        elif self.player_2 and self.player_2.player_id==player_id:
            return 2
        else:
            return -1
    
    def check_turn_player_identity(self)->int:
        return self.check_player_identity(self.turn_player)
    
    def check_is_full_players(self)->bool:
        if self.player_1 is None or self.player_2 is None:
            return False
        else:
            return True
    
    def check_command_player(self,player_id:int)->Player:
        # if self.player_1 is None or self.player_2 is None:
        #     return None
        if self.player_1 and self.player_1.player_id==player_id:
            return self.player_1
        elif self.player_2 and self.player_2.player_id==player_id:
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
            # event=event,
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