async function enterTestRoom(){
    const res=await fetch("/api/enter_room",{
       method:"POST",
       headers:{"Content-Type":"application/json"},
       body:JSON.stringify({room_id:"test_room_01",user_id:user_id,as_player:true})
    });

    const res_data=await res.json();
    if(res_data.ok){
        
    }
}