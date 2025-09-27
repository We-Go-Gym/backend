FROM python:3.10-slim

# Definir diretório de trabalho dentro do container (nível acima da pasta app)
WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação
COPY ./app /code/app

EXPOSE 8000

# Comando para rodar a aplicação usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]