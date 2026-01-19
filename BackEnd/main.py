from fastapi import FastAPI

app=FastAPI()

@app.get("/api/hello")
def root():
    return {"Message" : "BackEnd Is Running!"}