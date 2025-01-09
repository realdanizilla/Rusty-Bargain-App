# Dockerfile-backend

# Imagem base
FROM python:3.11

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos de dependências e instalar
#COPY requirements.txt /app/requirements.txt
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the logging configuration explicitly
#COPY logging_config.py /app/logging_config.py

# Copiar o restante dos arquivos do projeto
#COPY . /app
COPY . /app/backend

# setando token to logfire
ENV LOGFIRE_TOKEN=rZR2PJPQxzV73f2V24k6V6Ww9f3JpBv2T3P3x6qMWsDF
ENV PYTHONPATH=/app

# Comando para executar a aplicação
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["sh", "-c", "python data/seeder.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & python data/seeder.py && wait"]

