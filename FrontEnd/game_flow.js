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
    // receiveText(data.log);
    if(data.success){
        console.log(data.log)

    }
    else{
        console.error(data.log)
    }
}

function handleGameStart(data){
    console.log(data)
}

function handleFirstTurnplayer(data){
    console.log(data)
}

function handleDrawInitialHand(data){
    console.log(data)
}

function next_phase(){
    if(ws.readyState!==WebSocket.OPEN){
        console.error("WebSocket not open:",ws.readyState);
        return
    }
    console.log("Command Player ID: ",user_id)
    ws.send(JSON.stringify({
        type:"action",
        action:"next_phase"
    }));
}