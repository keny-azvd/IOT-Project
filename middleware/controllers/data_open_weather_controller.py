from fastapi import APIRouter, HTTPException, Request
from confluent_kafka import Producer, KafkaError
import json

router = APIRouter()

@router.get("/openweather")
async def get_users():
    return {"message": "Open Weather API"}

@router.post("/command/esp")
async def post_command_esp(request: Request):
    print("Received POST request to /command/esp")
    data = await request.json()

    esp_id = data.get("esp_id")
    actuator_id = data.get("actuator_id")
    command = data.get("command")  # Rota que será enviada como parte do comando

    print(f"ESP ID: {esp_id}, Actuator ID: {actuator_id}, Command: {command}")
    if not esp_id or not actuator_id or not command:
        raise HTTPException(status_code=400, detail="Missing 'esp_id', 'actuator_id', or 'route' in request body")

    print("Sending command to ESP")
    bootstrap_servers = 'kafka1:19091'
    conf = {
        'bootstrap.servers': bootstrap_servers
    }

    print(f"Connecting to Kafka broker at {bootstrap_servers}")
    producer = Producer(conf)
    topic = 'command_esp'

    print(f"Producing message to topic {topic}")
    # Compondo a mensagem em JSON incluindo a rota
    message = json.dumps({
        "esp_id": esp_id,
        "actuator_id": actuator_id,
        "command": "activate"  # Comando pode ser customizado
    })

    print("Message to be sent:", message)
    # Callback para tratar erros durante o envio de mensagens
    def delivery_report(err, msg):
        if err is not None:
            raise HTTPException(status_code=500, detail=f"Kafka error: {err.str()}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    try:
        # Envia a mensagem para o tópico com callback de entrega
        print("Sending message to Kafka")
        producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
        producer.flush()  # Aguarda até que todas as mensagens sejam enviadas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error producing message: {str(e)}")

    return {"message": "Command sent to ESP", "esp_id": esp_id, "actuator_id": actuator_id}
