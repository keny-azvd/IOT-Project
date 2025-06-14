from confluent_kafka import Producer
from dotenv import load_dotenv
import os

load_dotenv()

class ProducerMessage:
    def __init__(self):
        bootstrap_servers = 'kafka_kafka1_1:19091'
        self.conf = {
            'bootstrap.servers': bootstrap_servers
        }
        self.producer = Producer(self.conf)

    def delivery_report(self, err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
            print(f'Message key: {msg.key().decode("utf-8")}, value: {msg.value().decode("utf-8")}')

    def send_message(self, topic, key, value):
        self.producer.produce(topic, key=key, value=value, callback=self.delivery_report)
        self.producer.flush()
