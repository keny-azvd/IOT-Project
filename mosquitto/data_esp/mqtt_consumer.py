import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
import json
import pytz


class MQTTConsumer:
    def __init__(self, mongo_host, mongo_port, mongo_db_name, mongo_collection_name, topic, broker_ip, mqtt_port):
        # Configurações do MongoDB
        mongo_client = MongoClient(mongo_host, mongo_port)
        db = mongo_client[mongo_db_name]
        self.collection = db[mongo_collection_name]

        # Configurações do MQTT
        self.topic = topic
        self.broker_ip = broker_ip
        self.mqtt_port = mqtt_port


    def on_message(self, client, userdata, msg):
        mensagem = msg.payload.decode()
        print(f"Mensagem recebida no tópico {msg.topic}: {mensagem}")
        
        # Corrigir a string para um JSON válido, caso necessário
        mensagem_corrigida = mensagem.replace('esp1', '"esp1"')  # Adicionando aspas ao redor de esp1
        
        try:
            # Converter a string corrigida para JSON
            dados_json = json.loads(mensagem_corrigida)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar a mensagem: {e}")
            return
        brasilia_tz = pytz.timezone('America/Sao_Paulo')
        timestamp_brasilia = datetime.now(brasilia_tz).isoformat()

        # Gerar timestamp localmente
        data = {
            "timestamp": timestamp_brasilia,
            "name": dados_json["name"],
            "temperature": dados_json["temperature"],
            "humidity": dados_json["humidity"],
            "topico": msg.topic
        }

        # Inserir a mensagem no MongoDB
        result = self.collection.insert_one(data)
        print(f"Dado inserido com id: {result.inserted_id}")


    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao broker MQTT")
            client.subscribe(self.topic)
        else:
            print(f"Falha ao conectar, código de retorno {rc}")

    def on_log(self, client, userdata, level, buf):
        print(f"LOG: {buf}")

    def run(self):
        client = mqtt.Client(protocol=mqtt.MQTTv311)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_log = self.on_log

        print(f"Conectando ao broker no IP {self.broker_ip}")
        try:
            client.connect(self.broker_ip, self.mqtt_port)
        except Exception as e:
            print(f"Erro ao conectar ao broker: {e}")
            return
        client.loop_forever()

if __name__ == "__main__":
    consumer = MQTTConsumer(mongo_host="mongo-esp", mongo_port=27017, mongo_db_name="weather", mongo_collection_name="data_weather_esp", 
                            topic="data_weather_esp", broker_ip="mosquitto", mqtt_port=6082)
    
    consumer.run()
