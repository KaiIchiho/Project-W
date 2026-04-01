async function login(){
    const name_input=document.getElementById("user_name");
    const pw_input=document.getElementById("password");

    login_name=name_input.value;
    password=pw_input.value;

    if(login_name=="" || password==""){
        console.log("User Name Or Password Should Not Be None.");
        return;
    }
    console.log("input name: "+login_name, "input Password: "+password);

    const res=await fetch("/api/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            user_name:login_name,
            password:password
        })
    });
    const res_data=await res.json();
    if(res_data.success===true){
        user_id=res_data.user_id;
        user_name=res_data.user_name;

        name_input.value="";
        pw_input.value="";
        createWebSocket();
        console.log(res_data.log)
    }
    else{
        console.error(res_data.log)
    }
}
async function logout(){
    if(ws==null){
        return;
    }

    const res=await fetch("/api/logout",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({user_id:user_id})
    });
    const res_data=await res.json();
    if(res_data.success===true){
        //ws.close();
        console.log(res_data.log);
    }
}