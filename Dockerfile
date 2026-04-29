FROM python:3.11-slim

#WORKDIR /app

# Instala dependências de sistema (se o seu script precisar de bibliotecas C, como para bancos de dados)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o arquivo de dependências primeiro
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código fonte
COPY . .

# Comando para executar o script
CMD ["python", "script.py"]