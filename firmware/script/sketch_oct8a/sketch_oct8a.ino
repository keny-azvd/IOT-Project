#include <WiFi.h> 
#include <PubSubClient.h>
#include "dht.h" // Inclusão da biblioteca DHT

// Definições para conexão WiFi
const char* ssid = "dlink-9470";
const char* password = "jpjfi31862";

// Definições para MQTT
const char* mqtt_server = "192.168.0.104"; // Endereço do servidor MQTT
const int mqtt_port = 6082; // Porta MQTT
const char* mqtt_topic = "data_weather_esp"; // Tópico para enviar dados
const char* mqtt_topic_trigger = "trigger_esp1"; // Tópico para receber comandos
const char* mqtt_client_id = "esp_01"; // ID do cliente MQTT
const char* controler_name = "esp1";

// Configuração dos pinos
const int pinDHT11 = 12; // Pino do sensor DHT11
const int pinLed = 18; // Pino do LED

// Variáveis para controle de tempo
unsigned long lastPublishTime = 0; // Variável para armazenar o último tempo de publicação
const unsigned long publishInterval = 60000; // Intervalo de 60 segundos para publicar dados

// Inicialização do cliente MQTT
WiFiClient espClient;
PubSubClient client(espClient);

// Variável para o sensor DHT
dht DHT;

// Função para conectar ao broker MQTT
void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentando conectar ao MQTT...");
    if (client.connect(mqtt_client_id)) {
      Serial.println("Conectado");
      client.subscribe(mqtt_topic_trigger); // Assina o tópico trigger para receber mensagens
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

// Função callback para mensagens MQTT
void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Mensagem recebida em [");
  Serial.print(topic);
  Serial.print("]: ");
  
  String messageTemp;
  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }
  Serial.println(messageTemp);

  if (String(topic) == mqtt_topic_trigger) {
    if (messageTemp == "true") {
      digitalWrite(pinLed, HIGH); // Liga o LED
      Serial.println("LED ligado.");
    } else if (messageTemp == "false") {
      digitalWrite(pinLed, LOW); // Desliga o LED
      Serial.println("LED desligado.");
    }
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(pinLed, OUTPUT);
  digitalWrite(pinLed, LOW);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado ao WiFi");

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long currentMillis = millis();
  if (currentMillis - lastPublishTime >= publishInterval) {
    lastPublishTime = currentMillis;

    DHT.read11(pinDHT11); // Lê o sensor DHT11
    float temperature_sensor = DHT.temperature;
    float humidity_sensor = DHT.humidity;

    // Monta os dados JSON
    String sensorData = "{\"temperature\": ";
    sensorData += String(temperature_sensor, 1);
    sensorData += ", \"humidity\": ";
    sensorData += String(humidity_sensor, 1);
    sensorData += ", \"name\": ";
    sensorData += String(controler_name);
    sensorData += "}";

    client.publish(mqtt_topic, sensorData.c_str()); // Publica os dados no tópico MQTT
    Serial.println("Dados publicados: " + sensorData);
  }
}
