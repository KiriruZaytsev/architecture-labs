FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install poetry

RUN pip install --upgrade pip wheel setuptools

RUN pip install pycrypto

RUN poetry install --no-root

CMD ["poetry", "run", "python3", "src/main.py"]