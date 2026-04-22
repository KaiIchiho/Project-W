function directAttack(){
    attack("direct")
}

function frontAttack(){
    attack("front")
}

function sideAttack(){
    attack("side")
}

function attack(attack_type){
    console.log("attack,type:",attack_type)
    if (selected_stage_index.length === 0){return}
    let data={
        "client_common":{
            "event":"attack_phase_declare"
        },
        "stage_position_index":selected_stage_index[0],
        "attack_type":attack_type
    }
    sendJson(data)
}