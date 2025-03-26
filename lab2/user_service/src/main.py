import uvicorn
from fastapi import FastAPI

from auth import router as auth_router
from crud import router as user_router 

app = FastAPI(
    title="My Modular API",
    description="Пример FastAPI приложения с разделением на модули.",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    """Корневой эндпоинт."""
    return {"message": "Лабораторную выполнил студент группы М8О-114СВ-24 Зайцев Кирилл"}


if __name__ == '__main__':
    print("Starting server on http://0.0.0.0:8000")
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)