import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import User

app = FastAPI()

user_db = []

@app.get("/")
def read_root():
    return {"msg": "Hello, world!"}


@app.post("/user")
def create_user(user: User):
    for created_user in user_db:
        if created_user.id == user.id:
            raise HTTPException(status_code=404, detail="User not found!")
    user_db.append(user)
    return user


@app.get("/user/search/login")
def get_user_by_login(login: str) -> User:
    for user in user_db:
        if user.login == login:
            return user
    raise HTTPException(status_code=404, detail="User not found!")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)