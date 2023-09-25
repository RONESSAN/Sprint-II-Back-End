# Define a imagem base
FROM python:3.11.3

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o código-fonte para o diretório de trabalho
COPY . .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Define o comando de execução da API
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
