from models.player import Player
from typing import Optional

class Room():
    player_1:Optional[Player]=None
    player_2:Optional[Player]=None
    viewer:Optional[Player]=None
    def __init__(self,room_id:int,room_name:str):
        self.room_id=room_id
        self.room_name=room_name
    
    def set_players(self,player_1,player_2):
        self.player_1=player_1
        self.player_2=player_2
        
    def set_player_1(self,player_1):
        self.player_1=player_1
    def set_player_2(self,player_2):
        self.player_2=player_2
    def set_viewer(self,viewer):
        self.viewer=viewer
    
    def entered_as_player(self,player)->bool:
        if self.player_1 is None:
            self.set_player_1(player)
            return True
        else:
            if self.player_2 is None:
                self.set_player_2(player)
                return True
            else:
                print("Players full")
                return False
            
    def enter_as_viewer(self,viewer)->bool:
        if self.viewer is None:
            self.viewer=viewer
            return True
        else:
            return False
        
    def exit_by_id(self,player_id):
        result=False
        identity=-1
        if self.player_1 is not None:
            if self.player_1.player_id==player_id:
                self.player_1=None
                result=True
                identity=1
        if self.player_2 is not None:
            if self.player_2.player_id==player_id:
                self.player_2=None
                result=True
                identity=2
        if self.viewer is not None:
            if self.viewer.player_id==player_id:
                self.viewer=None
                result=True
                identity=3
        return result, identity

    def check_user_in_room(self,id)->bool:
        _is_player = self.check_player_in_room(id)
        _is_viewer = self.check_viewer_in_room(id)
        is_in_room = _is_player or _is_viewer
        return is_in_room
    
    def check_player_in_room(self,id)->bool:
        is_in_room=False
        if self.player_1 is not None:
            if self.player_1.player_id==id:
                is_in_room=True
        if self.player_2 is not None:
            if self.player_2.player_id==id:
                is_in_room=True
        return is_in_room
        
    def check_viewer_in_room(self,id)->bool:
        is_in_room=False
        if self.viewer is not None:
            if self.viewer.player_id==id:
                is_in_room=True
        return is_in_room
    
    def get_all_ids(self)->list[int]:
        ids:list[int]=[]
        if self.player_1 is not None:
            ids.append(self.player_1.player_id)
        if self.player_2 is not None:
            ids.append(self.player_2.player_id)
        if self.viewer is not None:
            ids.append(self.viewer.player_id)
        return ids
    
    def check_is_players_full(self)->bool:
        if self.player_1 is not None and self.player_2 is not None:
            return True
        else:
            return False
        
    def get_members_info(self)->list[dict]:
        members_info:list[dict]=[]
        if self.player_1 is not None:
            members_info.append({
                "user_id": self.player_1.player_id,
                "user_name": self.player_1.name, 
                "is_player": True,
                "select_deck": self.player_1.get_deck_name()})
        if self.player_2 is not None:
            members_info.append({
                "user_id": self.player_2.player_id,
                "user_name": self.player_2.name, 
                "is_player": True,
                "select_deck": self.player_2.get_deck_name()})
        if self.viewer is not None:
            members_info.append({
                "user_id": self.viewer.player_id,
                "user_name": self.viewer.name, 
                "is_player": False,
                "select_deck": None})
        return members_info