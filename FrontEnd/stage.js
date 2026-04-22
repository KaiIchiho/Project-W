let stage_buttons=[]
let selected_stage_index=[]
window.addEventListener("DOMContentLoaded", () => {
    initStage();
});

function initStage(){
    const stage=document.getElementById("stage");
    for(let i=0;i<5;++i){
        const btn=document.createElement("button");
        btn.textContent=i+1;
        stage_buttons.push(btn)
        btn.onclick=()=>{
            selected_stage_index.push(i);
            console.log("Selected Stage: ",selected_stage_index)
        }
        stage.appendChild(btn);
    }
}

function updateStage(stage_data){
    const stage_zone=document.getElementById("stage");
    stage_zone.innerHTML = "";
    stage_buttons=[]
    const cards=stage_data.cards
    for (let i=0;i<cards.length;++i) {
        console.log(cards[i]);
        const btn=document.createElement("button");
        if(cards[i].card_id==-1||
            cards[i].card_id===null||
            cards[i].card_id===undefined)
        {
            btn.textContent=i+1;
        }
        else{
            btn.textContent=cards[i].card_id;
        }
        btn.onclick=()=>{
            const index=selected_stage_index.indexOf(i);
            if (index !== -1) {
                selected_stage_index.splice(index, 1);
            }
            else{
                selected_stage_index.push(i);
            }
            console.log("Selected Stage: ",selected_stage_index)
        }
        stage_buttons.push(btn);
        stage_zone.appendChild(btn);
    }
    selected_stage_index=[]
}

function charPlay(){
    console.log("charPlay");
    let data={
        client_common:{
            event:"main_phase_char_play"
        },
        "chosen_hand_card":selected_btn_index[0],
        "stage_position":selected_stage_index[0]
    }
    sendJson(data);
}

function eventPlay(){
    console.log("eventPlay");
    let data={
        client_common:{
            event:"main_phase_event_play",
        },
        use_card: {
            hand_index:selected_btn_index[0],
        }
    }
    sendJson(data)
}

function charMove(){
    console.log("charMove");
    if(selected_stage_index.length<2){return}
    let data={
        "client_common":{
            event:"main_phase_char_move",
        },
        "stage_position":{
            "index": selected_stage_index[0],
        },
        "target_stage_position":{
            "index": selected_stage_index[1],
        }
    }
    sendJson(data)
}