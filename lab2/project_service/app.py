import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Hello, world!"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)