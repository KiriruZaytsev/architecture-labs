import uvicorn
from projects_schemas import Project
from fastapi import FastAPI, HTTPException

from projects_schemas import Project

app = FastAPI()
projects_db = []

@app.get("/")
def read_root():
    return {"msg": "Hello, world!"}


@app.post("/project")
def create_project(name: str) -> Project:
    for project in projects_db:
        if project.name == name:
            return project


@app.get("/project/search/name")
def find_project_by_name(name: str) -> Project:
    for project in projects_db:
        if project.name == name:
            return project
    raise HTTPException(status_code=404, detail="User not found!")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)