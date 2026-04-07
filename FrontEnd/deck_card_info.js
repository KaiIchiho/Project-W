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
    for (const deck of deck_list) {
        const opt = document.createElement("option");
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