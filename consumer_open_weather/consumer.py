from confluent_kafka import Consumer, KafkaError, KafkaException
from dotenv import load_dotenv
import os
from model import Model
import json
import datetime
load_dotenv()

class ConsumerWeather:
    def __init__(self):
        self.config = {
            'bootstrap.servers': os.getenv("KAFKA_SERVER"),
            'group.id': os.getenv("KAFKA_GROUP_ID"),
            'auto.offset.reset': os.getenv("KAFKA_OFFSET")
        }

        self.consume = Consumer(self.config)
        self.consume.subscribe([os.getenv("KAFKA_TOPIC")])
        self.model = Model()

    def consume_data(self):
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
                
                print('Received message: {}'.format(msg.value().decode('utf-8')))
                print('Data ------: {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                self.model.insert(json.loads(msg.value().decode('utf-8')))
        except KeyboardInterrupt:
            print("Interrupted by user")
        finally:
            self.consume.close()
            print("Consumer closed")

if __name__ == "__main__":
    consumer = ConsumerWeather()
    consumer.consume_data()