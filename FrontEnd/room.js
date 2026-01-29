let current_room_id;
async function enterTestRoom(isPlayer){
    room_id="test_room_01";
    
    const res=await fetch("/api/enter_room",{
       method:"POST",
       headers:{"Content-Type":"application/json"},
       body:JSON.stringify({room_id:room_id,user_id:user_id,as_player:isPlayer})
    });

    const res_data=await res.json();
    if(res_data.ok){
        /*const enter_menu=document.getElementById("enter_room_menu");
        const exit_menu=document.getElementById("exit_room_menu");
        enter_menu.style.display="none";
        exit_menu.style.display="block";*/
        setComponentHidden("enter_room_menu",true);
        setComponentHidden("exit_room_menu",false);

        const room_info=document.getElementById("room_info");
        let as_player;
        if(isPlayer)as_player="Player";
        else as_player="Viewer";
        room_info.textContent="Room ID: "+room_id+", As "+as_player;
        current_room_id=room_id;

        console.log("Enter Test Room Success");
        setComponentHidden("message_block",false);
    }
    else{
        console.error("Cannot Enter Test Room");
    }
}

async function exitTestRoom() {
    console.log("Exit Test Room ID: "+current_room_id+"User ID: "+user_id);
    const res=await fetch("/api/exit_room",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({room_id:current_room_id,user_id:user_id})
    });
    const res_data=await res.json();

    if(res_data.ok){
        /*const enter_menu=document.getElementById("enter_room_menu");
        const exit_menu=document.getElementById("exit_room_menu");
        enter_menu.style.display="block";
        exit_menu.style.display="none";*/
        setComponentHidden("enter_room_menu",false);
        setComponentHidden("exit_room_menu",true);
        current_room_id="";
        
        console.log("Exit Test Room Success");
        setComponentHidden("message_block",true);
    }
    else{
        console.error("Cannot Exit Test Room");
    }
}

function setComponentHidden(id,isHidden){
    /*component=document.getElementById(id);
    if(isHidden){
        component.style.display="none";
    }
    else{
        component.style.display="block";
    }*/
}