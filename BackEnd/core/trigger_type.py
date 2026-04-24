from enum import Enum

class TriggerType(str,Enum):
    NONE="none"
    SOUL="soul"
    POOL="pool"
    COMEBACK="comeback"
    RETURN="return"
    DRAW="draw"
    TREASURE="treasure"
    SHOT="shot"
    GATE="gate"
    STANDBY="standby"
    CHOICE="choice"
    DISCOVERY="discovery"
    CHANCE="chance"
    FOCUS="focus"
    
    SOULPLUS1="soulplus1"
    SOULPLUS2="soulplus2"