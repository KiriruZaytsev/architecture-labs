'''
Заглушка для базы данных
'''
from typing import List, Dict
from schemas import User 

user_db: List[User] = []

client_db: Dict[str, str] = {
    "admin": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
}