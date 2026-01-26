from models.player import Player
from typing import Optional

class Room():
    player_1:Optional[Player]=None
    player_2:Optional[Player]=None
    viewer:Optional[Player]=None
    def __init__(self):
        pass
    
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
        if self.viewer is not None:
            self.viewer=viewer
            return True
        else:
            return False