
function levelUp(){
    const value = document.getElementById("clock_index").value;
    if (isNaN(value)) {
        alert("不是数字");
        return;
    }
    console.log("levelUp:",value);
    let data={
        "client_common":{
            event:"level_up",
        },
        "chosen_clock_card":value
    }
    sendJson(data)
    setComponentHidden("level_up",true)
}