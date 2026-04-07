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
    default_opt.value="--Deck Name--";
    default_opt.textContent="--Deck Name--";
    deck_select.appendChild(default_opt);
    
    const deck_names = await getAllDeckNames();
    for (const name of deck_names) {
        const opt = document.createElement("option");
        opt.value = name;
        opt.textContent = name;
        room_id_select.appendChild(opt);
    }
}

async function getAllDeckNames(){
    let names=[];
    info_list=await deck_list()
    console.log("getAllDeckNames:")
    console.log(info_list)
    
    for(const info of info_list){
        console.log(info.deck_name)
        names.push(info.deck_name)
    }
    return names
}

async function deck_list() {
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