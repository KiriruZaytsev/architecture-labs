import uvicorn
from fastapi import FastAPI, HTTPException

from crud import projects_router

app = FastAPI()
app.include_router(projects_router)


@app.get("/")
def read_root():
    return {"msg": "Сервис проектов"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)