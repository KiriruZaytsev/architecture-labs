import typing as tp
from fastapi import APIRouter, HTTPException, status

from database import project_db
from schemas import Project, Task

projects_router = APIRouter(
    prefix='/projects',
    tags=['projects']
)

@projects_router.get('/{proejct_id}')
def get_project_by_id(project_id: int) -> Project:
    for project in project_db:
        if project.id == project_id:
            return project
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail='Project not found')


@projects_router.post('/project')
def create_project(project: Project) -> Project:
    for existing_project in project_db:
        if project.id == existing_project.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f'Project with id {project.id} already exists')
        project_db.append(project)
    return project


@projects_router.get('/task/{project_id}/{task_id}')
def get_task_by_id(project_id: int,
                   task_id: int) -> Task:
    for project in project_db:
        if project.id == project_id:
            for task in project.tasks:
                if task.id == task_id:
                    return Task
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f'Task with id {task_id} not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Project with id {project_id} not found')


@projects_router.get('/project/{project_id}/tasks')
def get_all_tasks(project_id: int) -> tp.List[Task]:
    for project in project_db:
        if project.id == project_id:
            return project.tasks
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Project with id {project_id} not found')
