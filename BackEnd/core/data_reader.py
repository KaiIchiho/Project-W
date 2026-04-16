from schemas import common,object
from db import card_repo
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game import Game
    from models.player import Player
    # from models.playmat import Playmat

class DataReader():
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
    
    @staticmethod
    def get_deck_data(player:"Player")->object.DeckData:
        if not player:
            return object.DeckData()
        if not player.playmat:
            return object.DeckData()
        if not player.playmat.deck:
            return object.DeckData()
        cards:list[int]=[]
        card_info_list=["card_id"]
        for card in player.playmat.deck.cards:
            if card is None:
                continue
            card_info=card.get_current_info_by_list(card_info_list)
            cards.append(card_info)
        
        return object.build_object_data(
            "deck",
            card_num=len(cards),
            cards=cards)
    
    @staticmethod
    def get_stage_data(player:"Player")->object.StageData:
        if not player:
            return object.StageData()
        if not player.playmat:
            return object.StageData()
        cards=[]
        card_info_list=[
            "card_id",
            "card_power",
            "card_soul",
            "card_cost",
            "card_level",
            "card_color",
            "card_trigger",
            "card_effect_text"]
        for card in player.playmat.stage:
            if card is not None:
                card_info=card.get_current_info_by_list(card_info_list)
                cards.append(card_info)
            else:
                cards.append({"card_info":-1})
        markers=[]
        marker_info_list=["card_id"]
        for marker in player.playmat.markers:
            if marker is not None:
                marker_info=[]
                for card in marker:
                    info=card.get_current_info_by_list(marker_info_list)
                    marker_info.append(info)
                markers.append(marker_info)
            else:
                markers.append([])
        return object.build_object_data(
            "stage",
            card_num=len(cards),
            cards=cards,
            markers=markers
        )
    
    @staticmethod
    def get_waiting_room_data(player:"Player")->object.WaitingRoomData:
        if not player:
            return object.WaitingRoomData()
        if not player.playmat:
            return object.WaitingRoomData()
        cards:list[int]=[]
        card_info_list=["card_id"]
        for card in player.playmat.waiting_room:
            if card is None:
                continue
            # cards.append(card.card_id)
            card_info=card.get_current_info_by_list(card_info_list)
            cards.append(card_info)
        
        return object.build_object_data(
            "waiting_room",
            card_num=len(cards),
            cards=cards)
    
    @staticmethod
    def get_hand_data(player:"Player")->object.HandData:
        if not player:
            return object.HandData()
        cards:list[int]=[]
        card_info_list=["card_id"]
        for card in player.hand:
            if card is None:
                continue
            # cards.append(card.card_id)
            card_info=card.get_current_info_by_list(card_info_list)
            cards.append(card_info)
        
        return object.build_object_data(
            "hand",
            card_num=len(cards),
            cards=cards)

    @staticmethod
    def get_clock_data(player:"Player")->object.ClockData:
        if not player:
            return object.ClockData()
        if not player.playmat:
            return object.ClockData()
        cards:list[int]=[]
        card_info_list=["card_id"]
        for card in player.playmat.clock:
            if card is None:
                continue
            # cards.append(card.card_id)
            card_info=card.get_current_info_by_list(card_info_list)
            cards.append(card_info)
        
        return object.build_object_data(
            "clock",
            card_num=len(cards),
            cards=cards)
    
    @staticmethod
    def get_level_data(player:"Player")->object.LevelData:
        if not player:
            return object.LevelData()
        if not player.playmat:
            return object.LevelData()
        cards:list[int]=[]
        card_info_list=["card_id"]
        for card in player.playmat.level:
            if card is None:
                continue
            # cards.append(card.card_id)
            card_info=card.get_current_info_by_list(card_info_list)
            cards.append(card_info)
        
        return object.build_object_data(
            "level",
            card_num=len(cards),
            cards=cards)
    
    @staticmethod
    def get_stock_data(player:"Player")->object.StockData:
        # player=game.check_command_player(player_id)
        if not player:
            return object.StockData()
        if not player.playmat:
            return object.StockData()
        cards:list[int]=[]
        card_info_list=["card_id"]
        for card in player.playmat.stock:
            if card is None:
                continue
            # cards.append(card.card_id)
            card_info=card.get_current_info_by_list(card_info_list)
            cards.append(card_info)
        
        return object.build_object_data(
            "stock",
            card_num=len(cards),
            cards=cards)
    
    @staticmethod
    def get_cx_data(player:"Player")->object.CXData:
        # player=game.check_command_player(player_id)
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
    
    @staticmethod
    def get_memory_data(player:"Player")->object.MemoryData:
        if not player:
            return object.MemoryData()
        if not player.playmat:
            return object.MemoryData()
        cards:list[int]=[]
        card_info_list=["card_id"]
        for card in player.playmat.memory:
            if card is None:
                continue
            # cards.append(card.card_id)
            card_info=card.get_current_info_by_list(card_info_list)
            cards.append(card_info)
        
        return object.build_object_data(
            "memory",
            card_num=len(cards),
            cards=cards)
    
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