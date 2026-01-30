let current_room_id;

const room_id_select=document.getElementById("room_id_select");
function bindEvents(){
    room_id_select.addEventListener("focus", () => {
        console.log("select focused");
        updateRoomIDOptions();
    });
}

async function updateRoomIDOptions(){
    console.log("RoomID Options Update");
    room_id_select
    select.innerHTML = "";

    const room_ids = await getAllRoomIDs();
    for (const id of room_ids) {
        const opt = document.createElement("option");
        opt.value = id;
        opt.textContent = id;
        select.appendChild(opt);
    }
}

async function getAllRoomIDs() {
    room_id_list;
    const res=await fetch("/api/get_room_id_list");
    if(!res.ok){
        console.error("fetch failed");
        throw new Error("fetch failed");
    }
    const room_ids=await res.json();

    return room_id_select;
}

async function createRoom() {
    const input_room_id=document.getElementById("input_room_id");
    room_id=input_room_id.value;
    input_room_id.value="";

    const res=await fetch("/api/create_room",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({room_id:room_id})
    });
    const res_data=await res.json();
    if(res.ok){

    }
    else{

    }
}

async function enterRoom(isPlayer){
    const room_id_select=document.getElementById("room_id_select");
    room_id=room_id_select.value

    const res=await fetch("/api/enter_room",{
       method:"POST",
       headers:{"Content-Type":"application/json"},
       body:JSON.stringify({room_id:room_id,user_id:user_id,as_player:isPlayer})
    });

    const res_data=await res.json();
    if(res_data.ok){
        setComponentHidden("enter_room_menu",true);
        setComponentHidden("exit_room_menu",false);

        const room_info=document.getElementById("room_info");
        let as_player;
        if(isPlayer)as_player="Player";
        else as_player="Viewer";
        room_info.textContent="Room ID: "+room_id+", As "+as_player;
        current_room_id=room_id;

        console.log("Enter Room "+room_id+" Success");
        setComponentHidden("message_block",false);
    }
    else{
        console.error("Cannot Enter Room "+room_id);
    }
}

async function exitRoom() {
    console.log("Exit Room ID: "+current_room_id+"User ID: "+user_id);
    const res=await fetch("/api/exit_room",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({room_id:current_room_id,user_id:user_id})
    });
    const res_data=await res.json();

    if(res_data.ok){
        setComponentHidden("enter_room_menu",false);
        setComponentHidden("exit_room_menu",true);
        current_room_id="";
        
        console.log("Exit Room Success");
        setComponentHidden("message_block",true);
    }
    else{
        console.error("Cannot Exit Room");
    }
}

function setComponentHidden(id,isHidden){
    component=document.getElementById(id);
    if(isHidden){
        component.style.display="none";
    }
    else{
        component.style.display="block";
    }
}