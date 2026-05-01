function handleSelectDeck(data){
    if(data.success===undefined||
        data.log===undefined)
    {
        return
    }
    // receiveText(data.log);
    if(data.success){
        console.log(data.log)

    }
    else{
        console.error(data.log)
    }

}

function handleStandby(data){
    if(data.success===undefined||
        data.log===undefined)
    {
        return
    }
    if(data.success){
        console.log(data.log)

    }
    else{
        console.error(data.log)
    }
}

function handleGameStart(data){
    // console.log(data)
}

function handleFirstTurnplayer(data){
    // console.log(data)
}

function handleDrawInitialHand(data){
    // console.log(data);
    let common=data.common;
    updateHandByCommon(common);
}

function handleSwapHandCards(data){
    console.log("New Hand");
    let common=data.common;
    updateHandByCommon(common)
}

function handleOnPhaseChanged(data){
    // console.log(data)
}

function handleShuffle(data){
    // console.log(data)
}

function handleLevelUp(data){
    setComponentHidden("level_up",false)
}

function handleStandPhaseAllStand(data){
    
}

function handleDrawPhaseDraw(data){
    // console.log(data)
    let common=data.common;
    updateHandByCommon(common);
}

function handleClockPhaseClock(data){
    let common=data.common;
    updateHandByCommon(common);
}

function handleClockPhaseDraw(data){
    let common=data.common;
    updateHandByCommon(common);
}

function handledMainPhaseCharPlay(data){
    let common=data.common;
    updateHandByCommon(common);
    let player1=common.player_1;
    let player2=common.player_2;
    let player;
    if(player1.user_id==user_id){
        player=player1;
    }
    else if(player2.user_id==user_id){
        player=player2;
    }
    updateStage(player.stage)
}

function handleMainPhaseEventPlay(data){
    let common=data.common;
    updateHandByCommon(common);
}

function handleMainPhaseCharMove(data){
    let common=data.common;
    let player1=common.player_1;
    let player2=common.player_2;
    let player;
    if(player1.user_id==user_id){
        player=player1;
    }
    else if(player2.user_id==user_id){
        player=player2;
    }
    updateStage(player.stage)
}

function handleClimaxPhaseCxSet(data){
    let common=data.common;
    let player1=common.player_1;
    let player2=common.player_2;
    let player;
    if(player1.user_id==user_id){
        player=player1;
    }
    else if(player2.user_id==user_id){
        player=player2;
    }
    updateHandByCommon(common)
    updateClimax(player)
}

function handleAttackPhaseDeclare(data){
    let common=data.common;
    let player1=common.player_1;
    let player2=common.player_2;
    let player;
    if(player1.user_id==user_id){
        player=player1;
    }
    else if(player2.user_id==user_id){
        player=player2;
    }
    updateStage(player.stage)
}

function handleAttackPhaseTriggerCheck(data){
    
}

function handleAttackPhaseCounterCheck(data){
    setComponentHidden("counter_check",false)
}

function handleAttackPhaseDamageCheck(data){
    
}

function handleAttackPhaseDamageProcess(data){
    
}

function handleAttackPhaseBattleProcess(data){
    let common=data.common;
    let player1=common.player_1;
    let player2=common.player_2;
    let player;
    if(player1.user_id==user_id){
        player=player1;
    }
    else if(player2.user_id==user_id){
        player=player2;
    }
    updateStage(player.stage)
}

function handleAttackPhaseEncore(data){
    let common=data.common;
    if(common.event_user_id===user_id){
        setComponentHidden("encore",false)
    }
}

function handleEndPhaseCxRemove(data){
    let common=data.common;
    let player1=common.player_1;
    let player2=common.player_2;
    let player;
    if(player1.user_id==user_id){
        player=player1;
    }
    else if(player2.user_id==user_id){
        player=player2;
    }
    updateClimax(player)
}

function handleEndPhaseHandExceed(data){
    
}

function handleEndPhaseHandDiscard(data){
    let common=data.common;
    let player1=common.player_1;
    let player2=common.player_2;
    let player;
    if(player1.user_id==user_id){
        player=player1;
    }
    else if(player2.user_id==user_id){
        player=player2;
    }
    updateHandByCommon(common)
}