
function cxSet(){
    if(selected_btn_index.length<1){return}
    let data={
        "client_common":{
            event:"climax_phase_cx_set",
        },
        "hand_index":selected_btn_index[0]
    }
    sendJson(data)
}

function updateClimax(player_data){
    cx=player_data.cx
    cx_button=document.getElementById("cx_button")
    if(cx.card_id===-1 || cx.card_id===null || cx.card_id===undefined){
        cx_button.textContent="Empty"
    }
    else{
        cx_button.textContent=cx.card_id
    }
}