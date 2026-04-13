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
    console.log(data)
}

function handleFirstTurnplayer(data){
    console.log(data)
}

function handleDrawInitialHand(data){
    // console.log(data);
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
    let hand=player.hand;
    let cards=hand.cards;
    for(const card of cards){
        console.log(card);
        addHand(card);
    }
}

function handleOnPhaseChanged(data){
    console.log(data.common)
}

function handleShuffle(data){
    console.log(data.common)
}

function nextPhase(){
    // if(ws.readyState!==WebSocket.OPEN){
    //     console.error("WebSocket not open:",ws.readyState);
    //     return
    // }
    // console.log("Command Player ID: ",user_id)
    // ws.send(JSON.stringify({
    //     type:"action",
    //     action:"next_phase"
    // }));
    console.log("nextPhase");
    data={
        client_common:{
            event:"next_phase"
        }
    }
    sendJson(data);
}