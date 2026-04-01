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
        // const log=document.getElementById("log");
        // log.innerHTML+="<p>"+event.data+"</p>";
        // console.log("Server back : ",event.data);
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
    if(!isDict(data)){
        console.error("Data Not Dict");
        return;
    }

    if(ws.readyState!==WebSocket.OPEN){
        console.error("WebSocket not open:",ws.readyState);
        return;
    }
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
            console.log(json_data)
            handleWsJson(json_data)
        }catch(e){
            // console.error("Parse JSON Failed:",e);
            const log=document.getElementById("log");
            log.innerHTML+="<p>"+data+"</p>";
            console.log("Server back : ",data);
        }
    }
}

event_method_dict={
    "enter_room":"handleEnterRoom",
    "exit_room":"handleExitRoom",
}

function handleWsJson(data){
    if(!isDict(data)){
        console.error("[handleWsJson] Data Not Dict");
        return;
    }
    if(data.event!==undefined){
        eve=data.event
        if(event_method_dict.eve!==undefined){
            const method=event_method_dict.eve
            window[method](data);
        }
    }
}