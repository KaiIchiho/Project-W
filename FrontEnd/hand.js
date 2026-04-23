let buttons=[];
let selected_card_id=-1;
let selected_btn_index=[];
// window.addEventListener("DOMContentLoaded", () => {
//     initButtonMap();
// });

// function initButtonMap(){
//     btn_card_id=new Map();
// }

function updateHandByCommon(common){
    let player1=common.player_1;
    let player2=common.player_2;
    let player;
    if(player1.user_id==user_id){
        player=player1;
    }
    else if(player2.user_id==user_id){
        player=player2;
    }
    let hand=player.hand;
    let cards=hand.cards;
    const hand_zone=document.getElementById("hand");
    hand_zone.innerHTML = "";
    buttons=[]
    selected_card_id=-1
    selected_btn_index=[]
    for(const card of cards){
        console.log(card);
        addHand(card.card_id);
    }
}

function addHand(card_id){
    const hand=document.getElementById("hand");
    const btn=document.createElement("button");
    btn.textContent=card_id;
    buttons.push(btn)
    btn.onclick=()=>{
        let index=buttons.indexOf(btn)
        if(index!==-1){
            let on_state=selectHandIndex(index);
            switchBtnState(btn,on_state);
            console.log(selected_btn_index)
            if(on_state){
                selected_card_id=card_id
            }
            else{
                selected_card_id=-1
            }
            console.log("selected_card_id: ",selected_card_id)
        }
    }
    hand.appendChild(btn);
}

function delHand(index){
    let btn=buttons[index];
    if(btn===undefined){
        console.error("button index[",index,"] not found");
        return;
    }
    buttons.splice(index,1);
    hand_card_id.splice(index,1)
    const hand=document.getElementById("hand");
    hand.removeChild(btn);
    btn.remove();
}

function switchBtnState(btn,is_on){
    if (!is_on) {
        btn.style.backgroundColor = ""; // 恢复默认
    } else {
        btn.style.backgroundColor = "yellow"; // 变黄色
    }
}

function selectHandIndex(index){
    let i_index=selected_btn_index.indexOf(index);
    if(i_index!==-1){
        selected_btn_index.splice(i_index,1)
        return false
    }
    else{
        selected_btn_index.push(index)
        return true
    }
}

function swapSelectedHandCards(){
    console.log("swapSelectedHandCards");
    let data={
        client_common:{
            event:"swap_hand_cards"
        },
        "hand_index":selected_btn_index,
    }
    sendJson(data);
    // selected_btn_index=[]
}

function clockSelectedHand(){
    console.log("clockSelectedHand")
    if (selected_btn_index.length === 0){return}
    let data={
        client_common:{
            event:"clock_phase_clock"
        },
        clocked_hand_card:{
            hand_index:selected_btn_index[0]
        }
    }
    sendJson(data);
}

function discardHand(){
    console.log("discardHand")
    let data={
        client_common:{
            event:"end_phase_hand_discard"
        },
        set_waiting_room:selected_btn_index
    }
    sendJson(data)
}