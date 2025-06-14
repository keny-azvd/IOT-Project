import requests
import json
from producer import ProducerMessage
from confluent_kafka import Consumer, KafkaError, KafkaException
from dotenv import load_dotenv
import os
import schedule
import time
load_dotenv()

class OpenWeather:
    def __init__(self, city = 'Sao Carlos', API_KEY = '7a9d681e6ad6eda2a170835984e7fff6'):
        self.city = city
        self.API_KEY = API_KEY
        self.link_call = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=pt_br"
    
    def get_data(self):
        request = requests.get(self.link_call)
        request_json = request.json()
        return request_json
    
    def send_data_weather(self):
        data = self.get_data()
        producer_message = ProducerMessage()
        data_bytes = json.dumps(data).encode('utf-8')
        producer_message.send_message("weather", "key", data_bytes)


schedule.every(30).minutes.do(OpenWeather().send_data_weather)
while True:
    schedule.run_pending()
    time.sleep(1)
