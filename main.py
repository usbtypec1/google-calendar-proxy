from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {"hello": "world"}

@app.get('/{name}')
def about(name: str):
    return {"hello": name}
