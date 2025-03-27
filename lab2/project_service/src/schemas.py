import typing as tp
from pydantic import BaseModel

class Task(BaseModel):
    id: int
    name: str
    description: str
    reporter_id: int
    assignee_id: int

class Project(BaseModel):
    id: int
    name: str
    owner: str
    users: tp.List[int]
    tasks: tp.List[Task]    