async function test_deck(params) {
    const res=await fetch(
        "api/test_deck",
        {
            method:"POST",
            header:{"Content-Type":"application/json"},
            body:JSON.stringify({})
        }
    )
}