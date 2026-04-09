let buttons=[];
let selected_btn_index=[];

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
    // buttons.set(btn,card_id);
    buttons.push(btn)
    btn.onclick=()=>{
        let index=buttons.indexOf(btn)
        if(index!==undefined){
            let on_state=selectHandIndex(index);
            switchBtnState(btn,on_state);
            print(selected_btn_index)
        }
    }
    hand.appendChild(btn);
}

function delHand(index){
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

function switchBtnState(btn,is_on){
    if (!is_on) {
        btn.style.backgroundColor = ""; // 恢复默认
    } else {
        btn.style.backgroundColor = "yellow"; // 变黄色
    }
}

function selectHandIndex(index){
    let i_index=selected_btn_index.indexOf(index);
    if(i_index!==undefined){
        selected_btn_index.slice(i_index,1)
        return false
    }
    else{
        selected_btns.push(index)
        return true
    }
}

function swapSelectedHandCards(){
    
}