from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from schemas import User
from database import user_db
from auth import get_current_client

router = APIRouter(
    prefix="/users", 
    tags=["users"], 
    dependencies=[Depends(get_current_client)]
)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: User,
                current_client: str = Depends(get_current_client)) -> User:
    """
    Создает нового пользователя. Требует аутентификации.
    """
    for existing_user in user_db:
        if existing_user.id == user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with id {user.id} already exists"
            )
        if existing_user.login == user.login:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with login '{user.login}' already exists"
            )

    user_db.append(user)
    print(f"Client '{current_client}' created user: {user}") 
    return user


@router.get("/search/login", response_model=User)
def get_user_by_login(login: str,
                      current_client: str = Depends(get_current_client)) -> User:
    """
    Ищет пользователя по логину. Требует аутентификации.
    """
    print(f"Client '{current_client}' searching for user with login: {login}")
    for user in user_db:
        if user.login == login:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/", response_model=List[User])
def get_all_users(current_client: str = Depends(get_current_client)):
    """Возвращает список всех пользователей."""
    return user_db


@router.get("/{user_id}", response_model=User)
def get_user_by_id(user_id: int, current_client: str = Depends(get_current_client)):
    """Возвращает пользователя по ID."""
    for user in user_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")