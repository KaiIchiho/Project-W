function standby(){
    if(ws.readyState!==WebSocket.OPEN){
        console.error("WebSocket not open:",ws.readyState);
        return
    }
    ws.send(JSON.stringify({
        event:"standby"
    }));
}

function handleStandby(data){
    if(data.success===undefined||
        data.log===undefined
    )
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