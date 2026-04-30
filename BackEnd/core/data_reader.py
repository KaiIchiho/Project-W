from schemas import common,object
from db import card_repo
from core.card_type import CardType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game
    from models.player import Player
    # from models.playmat import Playmat

class DataReader():
    @staticmethod
    def calculate_card_num_by_type(cards_type_info:list[dict]):
        char_card_num=0
        event_card_num=0
        cx_card_num=0
        for card_type in cards_type_info:
            if card_type.get("card_type") is None:
                continue
            if card_type.get("card_type")==CardType.CH.value:
                char_card_num+=1
            elif card_type.get("card_type")==CardType.EV.value:
                event_card_num+=1
            elif card_type.get("card_type")==CardType.CX.value:
                cx_card_num+=1
        return char_card_num,event_card_num,cx_card_num
    
    @staticmethod
    def read_card_colors(cards_color_info:list[dict])->list[str]:
        card_colors=[]
        for card_info in cards_color_info:
            color=card_info.get("card_color")
            if color is None:
                continue
            if color in card_colors:
                continue
            card_colors.append(color)
        return card_colors
    
    @staticmethod
    def get_common_data(
        game:"Game",
        success:bool,
        log:str,
        event_user_id:int
    )->common.CommonData:
        player_1=DataReader.get_player_data(game.player_1)
        player_2=DataReader.get_player_data(game.player_2)
        turn_player_user_id=-1
        if game.turn_player:
            turn_player_user_id=game.turn_player.player_id
        return common.CommonData(
            success=success,
            log=log,
            turn_player_user_id=turn_player_user_id,
            event_user_id=event_user_id,
            player_1=player_1,
            player_2=player_2)
    
    @staticmethod
    def get_player_data(player:"Player")->object.PlayerData:
        user_id=-1
        if player:
            user_id=player.player_id
        deck=DataReader.get_deck_data(player)
        stage=DataReader.get_stage_data(player)
        waiting_room=DataReader.get_waiting_room_data(player)
        hand=DataReader.get_hand_data(player)
        clock=DataReader.get_clock_data(player)
        level=DataReader.get_level_data(player)
        stock=DataReader.get_stock_data(player)
        cx=DataReader.get_cx_data(player)
        memory=DataReader.get_memory_data(player)
        resolution=DataReader.get_resolution_data(player)
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
            memory=memory,
            resolution=resolution)
    
    @staticmethod
    def get_deck_data(player:"Player")->object.DeckData:
        if not player:
            return object.DeckData()
        if not player.playmat:
            return object.DeckData()
        if not player.playmat.deck:
            return object.DeckData()
        card_info_list=["card_id"]
        cards_info=player.get_deck_cards_info_by_list(card_info_list)
        return object.build_object_data(
            "deck",
            card_num=len(cards_info),
            cards=cards_info)
    
    @staticmethod
    def get_stage_data(player:"Player")->object.StageData:
        if not player or not player.playmat:
            return object.StageData()
        card_info_list=[
            "card_id","card_power","card_soul",
            "card_cost","card_level","card_color",
            "card_trigger","card_effect_text"]
        stage_info=player.get_stage_cards_info_by_list(card_info_list)
        
        marker_info_list=["card_id"]
        marker_info=player.get_marker_cards_info_by_list(marker_info_list)
                
        stage_status=player.get_all_stage_status()
        return object.build_object_data(
            "stage",
            card_num=len(stage_info),
            cards=stage_info,
            stage_status=stage_status,
            markers=marker_info
        )
    
    @staticmethod
    def get_waiting_room_data(player:"Player")->object.WaitingRoomData:
        if not player:
            return object.WaitingRoomData()
        if not player.playmat:
            return object.WaitingRoomData()
        card_info_list=["card_id"]
        cards_info=\
            player.get_waiting_room_cards_info_by_list(card_info_list)
            
        card_type_info_list=["card_type"]
        cards_type_info=\
            player.get_waiting_room_cards_info_by_list(card_type_info_list)
        char_card_num,event_card_num,cx_card_num=\
            DataReader.calculate_card_num_by_type(cards_type_info)
        
        return object.build_object_data(
            "waiting_room",
            card_num=len(cards_info),
            char_card_num=char_card_num,
            event_card_num=event_card_num,
            cx_card_num=cx_card_num,
            cards=cards_info)
    
    @staticmethod
    def get_hand_data(player:"Player")->object.HandData:
        if not player:
            return object.HandData()
        card_info_list=[
            "card_id","card_power",
            "card_soul","card_cost",
            "card_level","card_color",
            "card_trigger","card_effect_text"]
        cards_info=player.get_hand_cards_info_by_list(card_info_list)
        
        return object.build_object_data(
            "hand",
            card_num=len(cards_info),
            cards=cards_info)

    @staticmethod
    def get_clock_data(player:"Player")->object.ClockData:
        if not player:
            return object.ClockData()
        if not player.playmat:
            return object.ClockData()
        card_info_list=["card_id"]
        cards_info=player.get_clock_cards_info_by_list(card_info_list)
        
        card_type_info_list=["card_type"]
        cards_type_info=\
            player.get_clock_cards_info_by_list(card_type_info_list)
        char_card_num,event_card_num,cx_card_num=\
            DataReader.calculate_card_num_by_type(cards_type_info)
        
        card_color_info_list=["card_color"]
        cards_color_info=player.get_clock_cards_info_by_list(card_color_info_list)
        card_colors=DataReader.read_card_colors(cards_color_info)
        
        return object.build_object_data(
            "clock",
            card_num=len(cards_info),
            char_card_num=char_card_num,
            event_card_num=event_card_num,
            cx_card_num=cx_card_num,
            cards=cards_info,
            card_colors=card_colors)
    
    @staticmethod
    def get_level_data(player:"Player")->object.LevelData:
        if not player:
            return object.LevelData()
        if not player.playmat:
            return object.LevelData()
        card_info_list=["card_id"]
        cards_info=player.get_level_cards_info_by_list(card_info_list)
        
        card_type_info_list=["card_type"]
        cards_type_info=\
            player.get_level_cards_info_by_list(card_type_info_list)
        char_card_num,event_card_num,cx_card_num=\
            DataReader.calculate_card_num_by_type(cards_type_info)
        
        card_color_info_list=["card_color"]
        cards_color_info=player.get_level_cards_info_by_list(card_color_info_list)
        card_colors=DataReader.read_card_colors(cards_color_info)
        
        return object.build_object_data(
            "level",
            card_num=len(cards_info),
            char_card_num=char_card_num,
            event_card_num=event_card_num,
            cx_card_num=cx_card_num,
            cards=cards_info,
            card_colors=card_colors)
    
    @staticmethod
    def get_stock_data(player:"Player")->object.StockData:
        # player=game.check_command_player(player_id)
        if not player:
            return object.StockData()
        if not player.playmat:
            return object.StockData()
        card_info_list=["card_id"]
        cards_info=player.get_stock_cards_info_by_list(card_info_list)
        
        card_type_info_list=["card_type","card_trigger"]
        cards_type_info=\
            player.get_stock_cards_info_by_list(card_type_info_list)
        char_card_num,event_card_num,cx_card_num=\
            DataReader.calculate_card_num_by_type(cards_type_info)
        cx_trigger=[]
        for i in range(len(cards_type_info)):
            if not cards_type_info[i].get("card_type")\
                or not cards_type_info[i].get("card_trigger"):
                continue
            if cards_type_info[i].get("card_type")==CardType.CX.value:
                cx_trigger.append(
                    {"index":i,
                     "trigger":cards_type_info[i].get("card_trigger")})
        
        return object.build_object_data(
            "stock",
            card_num=len(cards_info),
            char_card_num=char_card_num,
            event_card_num=event_card_num,
            cx_card_num=cx_card_num,
            cards=cards_info,
            cx_trigger=cx_trigger)
    
    @staticmethod
    def get_cx_data(player:"Player")->object.CXData:
        if not player:
            return object.CXData()
        if not player.playmat:
            return object.CXData()
        card_id:int=player.get_climax_id()
        
        return object.build_object_data(
            "cx",
            card_id=card_id)
    
    @staticmethod
    def get_memory_data(player:"Player")->object.MemoryData:
        if not player:
            return object.MemoryData()
        if not player.playmat:
            return object.MemoryData()
        card_info_list=["card_id"]
        cards_info=player.get_memory_cards_info_by_list(card_info_list)
        
        return object.build_object_data(
            "memory",
            card_num=len(cards_info),
            cards=cards_info)
    
    @staticmethod
    def get_resolution_data(player:"Player")->object.ResolutionData:
        if not player:
            return object.ResolutionData()
        
        if not player.playmat:
            return object.ResolutionData()
        card_info_list=["card_id"]
        cards_info=player.get_resolution_cards_info_by_list(card_info_list)
        
        return object.build_object_data(
            "resolution",
            card_num=len(cards_info),
            cards=cards_info)
    
    @staticmethod
    def get_add_card_data(card_id:int)->object.AddCardData:
        card_img=card_repo.read_card_field(card_id,"card_img")
        if card_img is None:
            card_img=""
        return object.build_object_data(
            "add_card",
            card_id=card_id,
            card_img=card_img
        )
        
    @staticmethod
    def get_stage_position_data_pack(index:int,is_empty:bool)->object.StageData:
        return object.build_object_data(
            "stage_position",
            index=index,
            is_empty=is_empty
        )