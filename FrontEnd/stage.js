let stage_buttons=[]
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
            
        }
        stage.appendChild(btn);
    }
}