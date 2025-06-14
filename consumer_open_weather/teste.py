import time
from confluent_kafka import Producer

# Configurações do produtor
conf = {
    'bootstrap.servers': '172.20.0.3:9092',  # Endereço do servidor Kafka
}

# Cria um produtor Kafka
producer = Producer(**conf)

# Função para enviar mensagens
def send_message():
    message = "Sua mensagem aqui"
    producer.produce('meu-topico', value=message)
    producer.flush()  # Garante que a mensagem foi enviada
    print(f"Mensagem enviada: {message}")

# Enviar uma mensagem a cada 1 minuto
while True:
    send_message()
    time.sleep(60)
