from ..models.player import Player
from .phase import Phase
from .attack_step import AttackStep
from typing import Callable

class Game():
    FLOW_LOGS:list[str]=[]
    PHASE_FLOW=[
        Phase.STAND,
        Phase.DRAW,
        Phase.CLOCK,
        Phase.MAIN,
        Phase.CLIMAX,
        Phase.ATTACK,
        Phase.END
    ]
    ATTACK_STEP_FLOW=[
        AttackStep.ATTACK_DECLARATION,
        AttackStep.TRIGGER,
        AttackStep.DAMAGE,
        AttackStep.BATTLE,
        AttackStep.ENCORE
    ]
    
    def __init__(self,
                 player_1:Player,
                 player_2:Player,
                 action_player:Player,
                 on_stand_phase_started:Callable[[Player],None],
                 on_draw_phase_started:Callable[[Player],None],
                 on_clock_phase_started:Callable[[Player],None],
                 on_main_phase_started:Callable[[Player],None],
                 on_climax_phase_started:Callable[[Player],None],
                 on_attack_phase_started:Callable[[Player],None],
                 on_end_phase_started:Callable[[Player],None],
                 on_ad_as_entered:Callable[[Player],None],
                 on_trigger_as_entered:Callable[[Player],None],
                 on_damage_as_entered:Callable[[Player],None],
                 on_battle_as_entered:Callable[[Player],None],
                 on_encore_as_entered:Callable[[Player],None],
                 ):
        if player_1 is player_2:
            raise ValueError("2 Player Are the Same")
        self.player_1=player_1
        self.player_2=player_2
        
        self.action_player=action_player
        self.current_turn=0
        self.current_phase:Phase
        self.current_attack_step:AttackStep
        
        self.on_stand_phase_started=on_stand_phase_started
        self.on_draw_phase_started=on_draw_phase_started
        self.on_clock_phase_started=on_clock_phase_started
        self.on_main_phase_started=on_main_phase_started
        self.on_climax_phase_started=on_climax_phase_started
        self.on_attack_phase_started=on_attack_phase_started
        self.on_end_phase_started=on_end_phase_started
        
        self.on_ad_as_entered=on_ad_as_entered
        self.on_trigger_as_entered=on_trigger_as_entered
        self.on_damage_as_entered=on_damage_as_entered
        self.on_battle_as_entered=on_battle_as_entered
        self.on_encore_as_entered=on_encore_as_entered
        
    def start_turn(self):
        self.current_turn+=1
        self.__start_phase(self.PHASE_FLOW(0))
    
    def start_next_turn(self):
        if self.action_player is self.player_1:
            self.action_player=self.player_2
        elif self.action_player is self.player_2:
            self.action_player=self.player_1
        
        self.current_turn+=1
        self.__start_phase(self.PHASE_FLOW(0))
        
        
    def start_next_phase(self):
        if self.current_phase in self.PHASE_FLOW:
            idx=self.PHASE_FLOW.index(self.current_phase)
            idx+=1
            if idx<len(self.PHASE_FLOW):
                self.__start_phase(self.PHASE_FLOW(idx))
            else: 
                self.__start_phase(self.PHASE_FLOW(0))
        else:
            return
    
    def enter_next_attack_step(self):
        if self.current_phase!=Phase.ATTACK:
            return
        if self.current_attack_step in self.ATTACK_STEP_FLOW:
            idx=self.ATTACK_STEP_FLOW.index(self.current_attack_step)
            idx+=1
            if idx<len(self.PHASE_FLOW):
                self.__start_phase(self.PHASE_FLOW(idx))
            else: 
                self.start_next_phase()
        else:
            return
        
    def __start_phase(self,next_phase:Phase):
        self.current_phase=next_phase
        
        new_log:str=""
        match next_phase:
            case Phase.STAND:
                new_log=self.__started_stand_phase()
            case Phase.DRAW:
                new_log=self.__started_draw_phase()
            case Phase.CLOCK:
                new_log=self.__started_clock_phase()
            case Phase.MAIN:
                new_log=self.__started_main_phase()
            case Phase.CLIMAX:
                new_log=self.__started_climax_phase()
            case Phase.ATTACK:
                new_log=self.__started_attack_phase()
            case Phase.END:
                new_log=self.__started_end_phase()
                
        self.FLOW_LOGS.append(new_log)
    
    def __enter_attack_step(self,next_attack_step:AttackStep):
        if self.current_phase!=Phase.ATTACK:
            return
        self.current_attack_step=next_attack_step
        
        new_log:str=""
        match next_attack_step:
            case AttackStep.ATTACK_DECLARATION:
                new_log=self.__entered_attack_declaration_step()
            case AttackStep.TRIGGER:
                new_log=self.__entered_trigger_step()
            case AttackStep.DAMAGE:
                new_log=self.__entered_damage_step()
            case AttackStep.BATTLE:
                new_log=self.__entered_battle_step()
            case AttackStep.ENCORE:
                new_log=self.__entered_encore_step()
                
        self.FLOW_LOGS.append(new_log)
        
    def __started_stand_phase(self):
        #self.current_phase=Phase.STAND
        self.on_stand_phase_started()
        return {"start_stand_phase"}
        
    def __started_draw_phase(self):
        #self.current_phase=Phase.DRAW
        self.on_draw_phase_started()
        return {"start_draw_phase"}
        
    def __started_clock_phase(self):
        #self.current_phase=Phase.CLOCK
        self.on_clock_phase_started()
        return {"start_clock_phase"}
        
    def __started_main_phase(self):
        #self.current_phase=Phase.MAIN
        self.on_main_phase_started()
        return {"start_main_phase"}
        
    def __started_climax_phase(self):
        #self.current_phase=Phase.CLIMAX
        self.on_climax_phase_started()
        return {"start_climax_phase"}
        
    def __started_attack_phase(self):
        #self.current_phase=Phase.ATTACK
        self.on_attack_phase_started()
        new_log=self.__enter_attack_step(self.ATTACK_STEP_FLOW(0))
        return {"start_attack_phase",new_log}
        
    def __started_end_phase(self):
        #self.current_phase=Phase.END
        self.on_end_phase_started()
        return {"start_end_phase"}
    
    
    def __entered_attack_declaration_step(self):
        #self.current_attack_step=AttackStep.ATTACK_DECLARATION
        self.on_ad_as_entered()
        return {"enter_attack_declaration_step"}
    
    def __entered_trigger_step(self):
        #self.current_attack_step=AttackStep.TRIGGER
        self.on_trigger_as_entered()
        return {"enter_trigger_step"}
    
    def __entered_damage_step(self):
        #self.current_attack_step=AttackStep.DAMAGE
        self.on_damage_as_entered
        return {"enter_damage_step"}
    
    def __entered_battle_step(self):
        #self.current_attack_step=AttackStep.BATTLE
        self.on_battle_as_entered()
        return {"enter_battle_step"}
    
    def __entered_encore_step(self):
        #self.current_attack_step=AttackStep.ENCORE
        self.on_encore_as_entered()
        return {"enter_encore_step"}