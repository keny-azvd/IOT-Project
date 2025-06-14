import paho.mqtt.client as mqtt
import time

class MQTTProducer:
    def __init__(self, broker, port):
        self.broker = broker
        self.port = port

    # Callback para verificar se a conexão foi bem-sucedida
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado com sucesso ao broker MQTT")
        else:
            print(f"Falha na conexão. Código de retorno: {rc}")

    def run(self, message, topic):
        client = mqtt.Client(protocol=mqtt.MQTTv311)

        # Define o callback para conexão
        client.on_connect = self.on_connect
        # Tenta conectar ao broker
        try:
            client.connect(self.broker, self.port)
            
            client.publish(topic, message)
            print(f"Mensagem enviada: {message}")

        except KeyboardInterrupt:
            print("\nSaindo...")

        finally:
            client.disconnect()


