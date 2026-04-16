function standby(){
    if(ws.readyState!==WebSocket.OPEN){
        console.error("WebSocket not open:",ws.readyState);
        return
    }
    ws.send(JSON.stringify({
        event:"standby"
    }));
}

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
    updateStage(common.stage)
}

function nextPhase(){
    console.log("nextPhase");
    let data={
        client_common:{
            event:"next_phase"
        }
    }
    sendJson(data);
}