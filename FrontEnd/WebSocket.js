//const ws=new WebSocket(`ws://${location.host}/api/ws`);
let ws=null;
let user_id;
let user_name;

function createWebSocket(){
    if(ws){
        ws.close();
    }

    ws=new WebSocket(`ws://${location.host}/api/ws`);
    ws.onopen=()=>{
        const login_info=document.getElementById("login_user_info");
        login_info.innerHTML="<p>"+"Logged-in User ID: "+user_id+", Name: "+user_name+"</p>";
        ws.send(user_id);
        
        setComponentHidden("login_menu",true);
        setComponentHidden("logout_menu",false);
        setComponentHidden("enter_room_menu",false);
        setComponentHidden("exit_room_menu",true);
        setComponentHidden("message_block",true);
        setComponentHidden("has_login_block",false);
        console.log("WebSocket Connect");
    }
    ws.onmessage=(event)=>{
        handleWsMessage(event)
    }
    ws.onerror = (err) => {
        console.error("WS error", err);
    };
    ws.onclose=async()=>{
        user_id="";
        user_name="";
        const login_info=document.getElementById("login_user_info");
        login_info.innerHTML="";
        
        setComponentHidden("login_menu",false);
        setComponentHidden("logout_menu",true);
        setComponentHidden("has_login_block",true);
        console.log("WebSocket Disconnect");
    }
}

function receiveText(text){
    if(typeof text!=="string"){
        return
    }
    console.log("receiveText")
    const log=document.getElementById("log");
    const p = document.createElement("p");
    p.textContent = text;
    log.appendChild(p);
    console.log("Server back : ",text);
}

function sendMessage(){
    if(ws.readyState!==WebSocket.OPEN){
        console.error("WebSocket not open:",ws.readyState);
        return;
    }
    const input=document.getElementById("input");
    ws.send(user_name+": "+input.value);
    console.log("Send : ",input.value+"\n");
    input.value="";
}

function isDict(obj) {
    return obj !== null && typeof obj === 'object' && !Array.isArray(obj);
}

function sendJson(data){
    console.log("sendJson")
    console.log(data)
    if(!isDict(data)){
        console.error("Data Not Dict");
        return;
    }

    if(ws.readyState!==WebSocket.OPEN){
        console.error("WebSocket not open:",ws.readyState);
        return;
    }
    
    console.log("Start WS Send Json")
    ws.send(JSON.stringify(data))
}

function handleWsMessage(event){
    const data=event.data
    if(data==null){
        console.warn("Null Data.");
        return;
    }
    if(typeof data==="string"){
        try{
            const json_data=JSON.parse(data)
            handleWsJson(json_data)
            if(json_data.log!==undefined){
                console.log("Data Has Log")
                receiveText(json_data.log)
            }
            else{
                console.error("Data No Log")
            }
        }catch(e){
            // console.error("Parse JSON Failed:",e);
            receiveText(data)
        }
    }
}

event_method_dict={
    "enter_room":"handleEnterRoom",
    "exit_room":"handleExitRoom",
    "select_deck":"handleSelectDeck",
    "standby":"handleStandby",
    "first_turnplayer":"handleFirstTurnplayer",
    "game_start":"handleGameStart",
    "game_end":"handleGameEnd",
    "determine_defeat":"handleDetermineDefeat",
    "draw_initial_hand":"handleDrawInitialHand",
    "swap_hand_cards":"handleSwapHandCards",
    "card_info":"handleCardInfo",
    "on_phase_changed":"handleOnPhaseChanged",
    "shuffle":"handleShuffle",
    "level_up":"handleLevelUp",
    "refresh":"handleRefresh",
    "stand_phase_all_stand":"handleStandPhaseAllStand",
    "draw_phase_draw":"handleDrawPhaseDraw",
    "clock_phase_clock":"handleClockPhaseClock",
    "clock_phase_draw":"handleClockPhaseDraw",
    "main_phase_char_play":"handledMainPhaseCharPlay",
    "main_phase_event_play":"handleMainPhaseEventPlay",
    "main_phase_char_move":"handleMainPhaseCharMove",
    "climax_phase_cx_set":"handleClimaxPhaseCxSet",
    "attack_phase_declare":"handleAttackPhaseDeclare",
    "attack_phase_trigger_check":"handleAttackPhaseTriggerCheck",
    "attack_phase_counter_check":"handleAttackPhaseCounterCheck",
    "attack_phase_damage_check":"handleAttackPhaseDamageCheck",
    "attack_phase_damage_process":"handleAttackPhaseDamageProcess",
    "attack_phase_battle_process":"handleAttackPhaseBattleProcess",
    "attack_phase_encore":"handleAttackPhaseEncore",
    "end_phase_cx_remove":"handleEndPhaseCxRemove",
    "end_phase_hand_exceed":"handleEndPhaseHandExceed",
    "end_phase_hand_discard":"handleEndPhaseHandDiscard"
}

function handleWsJson(data){
    if(!isDict(data)){
        console.error("[handleWsJson] Data Not Dict");
        return;
    }
    console.log("Handle Ws Json")
    if(data.event!==undefined){
        console.log("Data")
        console.log(data)
        eve=data.event
        handleWSDataByEvent(data,eve)
    }
    else if(data.common!==undefined){
        console.log("Common Data")
        console.log(data)
        common_data=data.common;
        if(common_data.event!==undefined){
            eve=common_data.event
            handleWSDataByEvent(data,eve)
        }
        if(common_data.log!==undefined){
            receiveText(common_data.log)
        }
    }
    else{
        console.error("Error Data")
        console.error(data)
    }
}

function handleWSDataByEvent(data,event){
    console.log("event: ",event);
    if(event in event_method_dict){
        const method=event_method_dict[event];
        console.log("method: ",method);
        console.log(data)
        window[method](data);
    }
}