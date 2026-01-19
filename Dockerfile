# Use uma imagem Linux estável e leve
FROM python:3.11-slim

# Evita arquivos temporários e logs travados
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código para dentro do container
COPY src/ src/

# Comando para rodar o app
CMD ["python", "src/main.py"]