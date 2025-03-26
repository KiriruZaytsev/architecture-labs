FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry install --no-root

CMD ["poetry", "run", "python3", "app.py"]