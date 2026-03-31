async function test_deck() {
    const res=await fetch(
        "api/test_deck",
        {
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({})
        }
    )
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