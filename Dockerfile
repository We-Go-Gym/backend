FROM python:3.10-slim

# Definir diretório de trabalho dentro do container (nível acima da pasta app)
WORKDIR /code

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY ./app /code/app

# Ele vai ou pegar a porta do railways ou a 8000 para testes locais
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"