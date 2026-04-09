let buttons=[];

// window.addEventListener("DOMContentLoaded", () => {
//     initButtonMap();
// });

// function initButtonMap(){
//     buttons=new Map();
// }

function addHand(card_id){
    const hand=document.getElementById("hand");
    const btn=document.createElement("button");
    btn.textContent=card_id;
    btn.onclick=()=>{
        selectHandCard(card_id);
    }
    // buttons.set(btn,card_id);
    buttons.push(btn)
    // hand.appendChild(btn);
}

function delHand(index){
    // buttons.delete(btn);
    btn=buttons[index];
    if(btn===undefined){
        console.error("button index[",index,"] not found");
        return;
    }
    buttons.splice(index,1);
    const hand=document.getElementById("hand");
    hand.removeChild(btn);
    btn.remove();
}

function selectHandCard(card_id){

}

function swapSelectedHandCards(){

}