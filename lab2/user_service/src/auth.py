from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DELTA, OAUTH2_TOKEN_URL
from database import client_db
from schemas import Token, TokenData

router = APIRouter(
    prefix="/auth",  # Префикс для всех путей в этом роутере
    tags=["authentication"] # Тег для документации Swagger/OpenAPI
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=OAUTH2_TOKEN_URL)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие простого пароля хешированному."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Хеширует пароль."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создает JWT токен доступа."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRE_DELTA
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_client(token: str = Depends(oauth2_scheme)) -> str:
    """
    Зависимость для проверки токена и получения имени текущего клиента (sub).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if username not in client_db:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Client not found or inactive',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    return username 


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Эндпоинт для получения JWT токена по имени пользователя и паролю.
    Использует стандартную форму OAuth2PasswordRequestForm.
    """
    client_username = form_data.username
    client_password = form_data.password

    hashed_password = client_db.get(client_username)

    if not hashed_password or not verify_password(client_password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    access_token = create_access_token(
        data={'sub': client_username}, expires_delta=ACCESS_TOKEN_EXPIRE_DELTA
    )
    return {'access_token': access_token, 'token_type': 'bearer'}