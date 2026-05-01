function standby(){
    if(ws.readyState!==WebSocket.OPEN){
        console.error("WebSocket not open:",ws.readyState);
        return
    }
    ws.send(JSON.stringify({
        event:"standby"
    }));
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

function levelUp(){
    const value = document.getElementById("clock_index").value;
    if (isNaN(value)) {
        alert("不是数字");
        return;
    }
    console.log("levelUp:",value);
    let data={
        "client_common":{
            event:"level_up",
        },
        "chosen_clock_card":Number(value)
    }
    sendJson(data)
    setComponentHidden("level_up",true)
}