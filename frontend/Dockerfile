# Dockerfile-frontend

# Imagem base
FROM python:3.11

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos de dependências e instalar
# COPY requirements.txt /app/requirements.txt
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Install backend as a Python package
COPY backend /app/backend
RUN pip install ./backend  # Executes setup.py automatically
COPY frontend /app/frontend

# Copiar o restante dos arquivos do projeto
COPY . /app/frontend

# Ensure backend folder is in the Python path
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Comando para executar a aplicação
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]