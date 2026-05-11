let current_room_id;

window.addEventListener("DOMContentLoaded", () => {
  bindEvents();
});

const room_id_select=document.getElementById("room_id_select");
function bindEvents(){
    room_id_select.addEventListener("focus", () => {
        console.log("select focused");
        updateRoomIDOptions();
    });
}

async function updateRoomIDOptions(){
    console.log("RoomID Options Update");
    room_id_select.innerHTML = "";
    const default_opt = document.createElement("option");
    default_opt.value="--Room ID--";
    default_opt.textContent="--Room ID--";
    room_id_select.appendChild(default_opt);
    
    const room_ids = await getAllRoomIDs();
    for (const id of room_ids) {
        const opt = document.createElement("option");
        opt.value = id;
        opt.textContent = id;
        room_id_select.appendChild(opt);
    }
}

async function getAllRoomIDs() {
    const res=await fetch("/api/get_room_id_list");
    if(!res.ok){
        console.error("fetch failed");
        throw new Error("fetch failed");
    }
    const room_id_list=await res.json();

    return room_id_list;
}

async function enterRoom(isPlayer){
    console.log("Enter Room Start");
    const room_id_select=document.getElementById("room_id_select");
    room_id_str=room_id_select.value
    let room_id = +room_id_str;
    if(room_id===NaN){
        console.error("Room ID Not Intiager");
        return;
    }
    let data={
        event:"enter_room",
        room_id:room_id,
        user_is_player:isPlayer
    }
    sendJson(data)
}

function handleEnterRoom(data){
    console.log("Handle Enter Room")
    if(data.success===undefined||
        data.user_is_player===undefined||
        data.room_id===undefined||
        data.log===undefined
    )
    {
        return;
    }
    if(data.success){
        setComponentHidden("enter_room_menu",true);
        setComponentHidden("exit_room_menu",false);

        const room_info=document.getElementById("room_info");
        let as_player;
        if(data.user_is_player)as_player="Player";
        else as_player="Viewer";
        room_info.textContent="Room ID: "+data.room_id+", As "+as_player;
        current_room_id=data.room_id;

        setComponentHidden("message_block",false);
    }
    else{
        // console.error("Cannot Enter Room "+room_id);
        console.error(data.log)
    }
}

async function exitRoom() {
    console.log("Exit Room ID: "+current_room_id+"User ID: "+user_id);

    data={
        event:"exit_room",
        user_id:user_id
    }
    sendJson(data)
}

function handleExitRoom(data){
    if(data.success===undefined||
        data.room_id===undefined||
        data.log===undefined
    )
    {
        return;
    }
    if(data.success && data.user_id===user_id){
        document.getElementById("log").innerHTML="";

        setComponentHidden("enter_room_menu",false);
        setComponentHidden("exit_room_menu",true);
        current_room_id="";
        
        console.log("handleExitRoom Data: ",data.log)
        setComponentHidden("message_block",true);
    }
    else{
        console.error(data.log)
    }
}

function setComponentHidden(id,isHidden){
    console.log("setComponentHidden",id)
    console.log("Is Hidden",isHidden)
    component=document.getElementById(id);
    if(isHidden){
        component.style.display="none";
    }
    else{
        component.style.display="block";
    }
}