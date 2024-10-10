# Use a imagem oficial do Python como base
FROM python:3.10-slim

# Instala o Poetry
RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Define o diretório de trabalho dentro do container
WORKDIR /code

# Copia os arquivos de dependências do Poetry para o diretório de trabalho
COPY pyproject.toml poetry.lock ./
COPY ./app /code/app

# Instala as dependências do projeto
RUN poetry install --no-root  && rm -rf $POETRY_CACHE_DIR

# Copia o restante do código da aplicação para o diretório de trabalho

# Define a variável de ambiente para desativar a criação de bytecode
ENV PYTHONDONTWRITEBYTECODE 1

# Define a variável de ambiente para desativar o buffer do stdout e stderr
ENV PYTHONUNBUFFERED 1

# Expõe a porta em que a aplicação irá rodar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]