from confluent_kafka import Consumer, KafkaError, KafkaException
import datetime
from mqtt_producer import MQTTProducer
import json


class ConsumerWeather:
    def __init__(self):
        self.config = {
            'bootstrap.servers': 'kafka_kafka1_1:19091',
            'group.id': 'weather_group',
            'auto.offset.reset': 'earliest'
        }

        self.consume = Consumer(self.config)
        self.consume.subscribe(['command_esp'])
        self.producer = MQTTProducer('mosquitto', 6082)

    def consume_data(self):
        print("Consumer running")
        try:
            while True:
                msg = self.consume.poll(timeout=1.0)
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())

                # Decodificando a mensagem do Kafka (msg.value() é um objeto bytes)
                kafka_message = json.loads(msg.value().decode('utf-8'))  # Converte de bytes para JSON
                
                # Agora você pode acessar os dados como um dicionário
                name = kafka_message.get("name")
                command = kafka_message.get("command")
                
                if not name or command is None:
                    print(f"Invalid message received: {kafka_message}")
                    continue

                # Construa o tópico MQTT dinamicamente com base no nome do Kafka
                topic_mqtt = f"trigger_{name}"

                # Enviar para o MQTT
                print(f"Sending to MQTT topic {topic_mqtt} with message {command}")
                self.producer.run(command, topic_mqtt)  # Ajuste conforme o método do seu MQTT Producer
                
                print(f"Message sent to {topic_mqtt}: {command}")
                
        except Exception as e:
            print(f"Error consuming data: {str(e)}")
if __name__ == "__main__":
    consumer = ConsumerWeather()
    consumer.consume_data()