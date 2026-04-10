window.addEventListener("DOMContentLoaded", () => {
  bindDeckSelectEvents();
});

const deck_select=document.getElementById("deck_select");
function bindDeckSelectEvents(){
    deck_select.addEventListener("focus", () => {
        console.log("select focused");
        updateDeckOptions();
    });
}

async function updateDeckOptions(){
    console.log("Deck Options Update");
    deck_select.innerHTML = "";
    const default_opt = document.createElement("option");
    default_opt.value=-1;
    default_opt.textContent="--Deck Name--";
    deck_select.appendChild(default_opt);
    
    const deck_list = await getDeckList();
    console.log(deck_list)
    for (const deck of deck_list) {
        const opt = document.createElement("option");
        console.log("deck_id: ",deck.deck_id);
        opt.value = deck.deck_id;
        opt.textContent = deck.deck_name;
        deck_select.appendChild(opt);
    }
}

// async function getAllDeckIDs(){
//     let names=[];
//     info_list=await deck_list()
//     console.log("getAllDeckNames:")
//     console.log(info_list)
    
//     for(const info of info_list){
//         console.log(info.deck_name)
//         names.push(info.deck_name)
//     }
//     return names
// }

async function getDeckList() {
    const res=await fetch(
        "api/deck_list",
        {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({})
        }
    );

    const res_data=await res.json();
    console.log(res_data);
    return res_data.deck_list;
}

async function test_card() {
    const res=await fetch(
        "api/test_card",
        {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({})
        }
    )
}

async function setDeck(){
    console.log("setDeck");
    const deck_select=document.getElementById("deck_select");
    let select_deck=+deck_select.value
    // let room_id = +room_id_str;
    if(select_deck===NaN){
        console.error("Deck ID Not Intiager");
        return;
    }
    data={
        event:"select_deck",
        select_deck:select_deck
    }
    sendJson(data)
}

async function readCardInfo(){
    console.log("readCardInfo");
    if (0 == hand_card_id.length) {
        return;
    }
    let card_id=hand_card_id[0];
    let data={
        event:"card_info",
        card_id:card_id,
        columns:["card_img", "card_color", "card_trigger", "card_power"]
    }
    sendJson(data)
}

function handleCardInfo(data){
    receiveText(data.columns)
}