function standby(){
    if(!ws){
        return
    }
    ws.send(JSON.stringify({
        type:"standby"
    }));
}