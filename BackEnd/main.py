from fastapi import FastAPI

app=FastAPI()

@app.get("/api/hello")
def root():
    a=step_one()
    b=step_two()
    return {"Message" : "BackEnd Is Running!", "a" : a, "b" : b}

def step_one():
    return "one"

def step_two():
    return "two"