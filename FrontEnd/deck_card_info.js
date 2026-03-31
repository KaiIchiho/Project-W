async function deck_list() {
    const res=await fetch(
        "api/test_deck",
        {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({})
        }
    )

    const res_data=await res.json()
    console.log(res_data)
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