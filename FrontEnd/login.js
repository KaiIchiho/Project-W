//const ws=new WebSocket(`ws://${location.host}/api/ws`);
let ws=null;
let user_id;
let user_name;
function createWebSocket(){
    if(ws){
        ws.close();
    }

    ws=new WebSocket(`ws://${location.host}/api/ws`);
    ws.onopen=()=>{
        const login_info=document.getElementById("login_user_info");
        login_info.innerHTML="<p>"+"Logged-in User ID: "+user_id+", Name: "+user_name+"</p>";
        ws.send(user_id);
        console.log("WebSocket Connect");
    }
    ws.onmessage=(event)=>{
        const log=document.getElementById("log");
        log.innerHTML+="<p>"+event.data+"</p>";
        console.log("Server back : ",event.data);
    }
    ws.onerror = (err) => {
        console.error("WS error", err);
    };
    ws.onclose=()=>{
        user_id="";
        user_name="";
        console.log("WebSocket Disconnect");
    }
}
function sendMessage(){
    if(ws.readyState!==WebSocket.OPEN){
        console.error("WebSocket not open:",ws.readyState);
        return;
    }
    const input=document.getElementById("input");
    ws.send(user_name+": "+input.value);
    console.log("Send : ",input.value+"\n");
    input.value="";
}

async function login(){
    const id_input=document.getElementById("user_id");
    const name_input=document.getElementById("user_name");

    id=id_input.value;
    name=name_input.value,
    console.log("input Id: "+id,"input name: "+name);

    const res=await fetch("/api/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({user_id:id,user_name:name})
    });
    const res_data=await res.json();
    if(res_data.ok===true){
        user_id=res_data.user_id;
        user_name=res_data.user_name;
        createWebSocket();

        id_input.value="";
        name_input.value="";
        const log_button=document.getElementById("log_button");
        log_button.innerHTML="<button onclick='logout()'>Logout</button>";
    }
}
async function logout(){
    if(ws==null){
        return;
    }

    const res=await fetch("/api/logout",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({user_id:id})
    });
    const res_data=await res.json();
    if(res_data.ok===true){
        ws.close();
        const log_button=document.getElementById("log_button");
        log_button.innerHTML="<button onclick='login()'>Login</button>";
        const login_info=document.getElementById("login_user_info");
        login_info.innerHTML="";
    }
}