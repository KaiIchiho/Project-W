from typing import Optional
import random
from ..core.game import Game
from ..models.player import Player
from ..models.playmat import Playmat
from ..models.card import Card
from ..models.deck import Deck

class EVETest():
    def __init__(self,
                 card_list_1:list[Card],
                 card_list_2:list[Card]):
        self.deck_1=Deck("Deck_01","Deck_1",card_list_1)
        self.deck_2=Deck("Deck_02","Deck_2",card_list_2)
        
        self.playmat_1=Playmat("Playmet_01","Playmet_1",self.deck_1)
        self.playmat_2=Playmat("Playmet_02","Playmet_2",self.deck_2)
        
        self.player_1=Player(
            "Player_01","Computer_1",self.playmat_1)
        self.player_2=Player(
            "Player_02","Computer_2",self.playmat_2)
        
        self.game_flow:Optional[Game]=None
        
    def start_game(self):
        self.__players_deck_shuffle()
        first_player=self.__decide_the_players_order()
        self.__init_players_hand()
        self.__manage_players_hand()
        
        self.game_flow=Game(
            self.player_1,
            self.player_2,
            first_player,
            self.on_stand_phase_started,
            self.on_draw_phase_started,
            self.on_clock_phase_started,
            self.on_main_phase_started,
            self.on_climax_phase_started,
            self.on_attack_phase_started,
            self.on_end_phase_started,
        )
    
    def __players_deck_shuffle(self):
        self.deck_1.shuffle()
        self.deck_2.shuffle()
    
    def __decide_the_players_order(self)->Player:
        WIN = {
            (0, 1),  # rock beats scissors
            (1, 2),  # scissors beats paper
            (2, 0),  # paper beats rock
        }
        a, b = random.sample([0, 1, 2], 2)
        if (a, b) in WIN:
            return self.player_1
        else:
            return self.player_2

    def __init_players_hand(self):
        self.player_1.init_hand()
        self.player_2.init_hand()
        
    def __manage_players_hand(self):
        num_1=random.randint(0,5)
        num_2=random.randint(0,5)
        manage_cards_1=random.sample(self.player_1.hand,num_1)
        manage_cards_2=random.sample(self.player_2.hand,num_2)
        self.player_1.manage_hand(manage_cards_1)
        self.player_2.manage_hand(manage_cards_2)
        
    def on_stand_phase_started(self,action_player:Player):
        new_log=f"{action_player.name} is in the stand phase."
        action_player
        
    def on_draw_phase_started(self,action_player:Player):
        new_log=f"{action_player.name} is in the draw phase."
        
    def on_clock_phase_started(self,action_player:Player):
        new_log=f"{action_player.name} is in the clock phase."
        
    def on_main_phase_started(self,action_player:Player):
        new_log=f"{action_player.name} is in the main phase."
        
    def on_climax_phase_started(self,action_player:Player):
        new_log=f"{action_player.name} is in the climax phase."
        
    def on_attack_phase_started(self,action_player:Player):
        new_log=f"{action_player.name} is in the attack phase."
        
    def on_end_phase_started(self,action_player:Player):
        new_log=f"{action_player.name} is in the end phase."