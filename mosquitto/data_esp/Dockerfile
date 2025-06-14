# Usar uma imagem base do Python
FROM python:3.12.5

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o script do consumer para o container
COPY mqtt_consumer.py .

# Instalar a biblioteca paho-mqtt
RUN pip install --no-cache-dir paho-mqtt pymongo python-dotenv   pytz


# Comando para executar o consumer
CMD ["python", "mqtt_consumer.py"]
