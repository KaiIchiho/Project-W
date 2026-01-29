from models.player import Player
from typing import Optional

class Room():
    room_id:str=""
    player_1:Optional[Player]=None
    player_2:Optional[Player]=None
    viewer:Optional[Player]=None
    def __init__(self,room_id:str):
        self.room_id=room_id
    
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
        
    def exit_by_id(self,player_id)->bool:
        result=False
        if self.player_1 is not None:
            if self.player_1.player_id==player_id:
                self.player_1=None
                result=True
        if self.player_2 is not None:
            if self.player_2.player_id==player_id:
                self.player_2=None
                result=True
        if self.viewer is not None:
            if self.viewer.player_id==player_id:
                self.viewer=None
                result=True
        return result
    
    def check_user_in_room(self,id)->bool:
        is_in_room=self.check_player_in_room(id) or self.check_viewer_in_room(id)
        return is_in_room
    
    def check_player_in_room(self,id)->bool:
        is_in_room=False
        if self.player_1 is not None:
            if self.player_1.id==id:
                is_in_room=True
        if self.player_2 is not None:
            if self.player_2.id==id:
                is_in_room=True
        return is_in_room
        
    def check_viewer_in_room(self,id)->bool:
        is_in_room=False
        if self.viewer is not None:
            if self.viewer.id==id:
                is_in_room=True
        return is_in_room
    
    def get_all_ids(self)->list[str]:
        ids:list[str]=[]
        if self.player_1 is not None:
            ids.append(self.player_1.player_id)
        if self.player_2 is not None:
            ids.append(self.player_2.player_id)
        if self.viewer is not None:
            ids.append(self.viewer.player_id)
        return ids