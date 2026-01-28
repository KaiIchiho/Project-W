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
        const enter_menu=document.getElementById("enter_room_menu");
        const exit_menu=document.getElementById("exit_room_menu");
        //enter_menu.hidden=false;
        //exit_menu.hidden=true;
        enter_menu.style.display="none";
        exit_menu.style.display="block";
        console.log(enter_menu.hidden, exit_menu.hidden);

        const room_info=document.getElementById("room_info");
        let as_player;
        if(isPlayer)as_player="Player";
        else as_player="Viewer";
        room_info.textContent="Room ID: "+room_id+", As "+as_player;
        current_room_id=room_id;

        console.log("Enter Test Room Success");
    }
    else{
        console.error("Cannot Enter Test Room");
    }
}

async function exitTestRoom() {
    const res=await fetch("/api/exit_room",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({user_id:user_id,as_player:isPlayer})
    });
    const res_data=await res.json();

    if(res_data.ok){
        const enter_menu=document.getElementById("enter_room_menu");
        const exit_menu=document.getElementById("exit_room_menu");
        //enter_menu.hidden=true;
        //exit_menu.hidden=false;
        enter_menu.style.display="block";
        exit_menu.style.display="none";
        console.log(enter_menu.hidden, exit_menu.hidden);
        current_room_id="";

        console.log("Exit Test Room Success");
    }
    else{
        console.error("Cannot Exit Test Room");
    }
}