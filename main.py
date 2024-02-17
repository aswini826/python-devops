from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello aswini"}

@app.get("/post")
def get_post():
    return {"message": "This is your posts"}

@app.post("/create")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new-post": f"Movie: {payload['Movie']} Genre: {payload['Genre']} Rating: {payload['Rating']}"}