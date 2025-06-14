from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import json
from models.model import Model
from models.model import Model as mod
from confluent_kafka import Producer
from bson import json_util

print("Iniciando aplicação Flask")

Model = Model(collection_name="mcus")
Model_dataweather = mod(collection_name="data_weather")
Model_data_esp = mod(collection_name="data_weather_esp")

app = Flask(__name__)
CORS(app, origins='*')

# Definindo a classe de DTO
class McuDto:
    def __init__(self, name: str):
        self.name = name

@app.route("/weather/all", methods=["GET"])
def get_all_data():
    try:
        data = Model_dataweather.get()
        print(data)

        temperatures = []
        humidities = []
        list_datetime = []
        for i in range(len(data)):
            temperatures.append(round(data[i]['main']['temp'] - 273.15, 2))
            humidities.append(round(data[i]['main']['humidity'], 2))
            list_datetime.append(data[i]['dt'])
        
        temperatures.reverse()
        humidities.reverse()
        list_datetime.reverse()

        data = {
            "temperatures": temperatures,
            "humidities": humidities,
            "datetime": list_datetime
        }

        return jsonify(data)

    except Exception as e:        
        print(f"Erro ao buscar dados: {e}")
        return jsonify({"message": "Erro ao buscar dados!"}), 500


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Welcome to the Flask MVC App!"})


@app.route("/mcu/<name>", methods=["POST"])
def create_item():
    data = request.get_json()
    name = data.get('name')
    actuator_status = False
    data = {
        "name": name,
        "actuator_status": actuator_status
    }
    if not name:
        abort(400, description="Name is required")

    existing_name_mcu = Model.get_one({"name": name})
    if existing_name_mcu:
        abort(400, description="Name already exists!")

    print(f"Inserindo dados: {data}")
    Model.insert(data)
    return jsonify({"message": "Data inserted successfully!"})

@app.route("/mcu/<name>/data_weather", methods=["GET"])
def get_last_temperature_and_humidity(name):
    try:
        data = Model_data_esp.get_last_temperature_and_humidity({"name": name})
        if not data:
            abort(404, description="Name not found!")
        return json.loads(json_util.dumps(data))
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return jsonify({"message": "Erro ao buscar dados!"}), 500

@app.route("/mcu/<name>/list_data_weather", methods=["GET"])
def get_list_temperature_and_humidity(name):
    try:
        data = Model_data_esp.get_lasts_temperature_and_humidity_by_name(name=name)
        if not data:
            abort(404, description="Name not found!")
        data.reverse()
        result = {
            "temperature": [item["temperature"] for item in data],
            "humidity": [item["humidity"] for item in data],
            "timestamp": [item["timestamp"] for item in data]
        }
        
        return jsonify(result)
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return jsonify({"message": "Erro ao buscar dados!"}), 500
        

@app.route("/mcu/all", methods=["GET"])
def get_all():
    return json.loads(json_util.dumps(Model.get()))

@app.route("/mcu/<name>", methods=["GET"])
def get_one(name):
    data = Model.get_one({"name": name})
    if not data:
        abort(404, description="Name not found!")
    return json.loads(json_util.dumps(data))


@app.route("/mcu/<name>", methods=["PUT"])
def update_one(name):
    data = request.get_json()
    existing_name_mcu = Model.get_one({"name": name})
    if not existing_name_mcu:
        abort(404, description="Name not found!")
    
    Model.update({"name": name}, data)
    return jsonify({"message": "Data updated successfully!"})


@app.route("/mcu/<name>", methods=["DELETE"])
def delete_one(name):
    existing_name_mcu = Model.get_one({"name": name})
    if not existing_name_mcu:
        abort(404, description="Name not found!")
    
    Model.delete({"name": name})
    return jsonify({"message": "Data deleted successfully!"})


@app.route("/command/<name>", methods=["PUT"])
def post_command_esp(name):
    print("Received POST request to /command/esp")
    
    # Obtenha os dados JSON
    data = request.get_json()

    # Pegue o valor de 'actuator_status' do JSON
    command = data.get("actuator_status")

    # Valide os parâmetros 'name' e 'command'
    if not name or command is None:
        abort(400, description="Missing 'name' or 'actuator_status' in request body")

    print(f"Sending command to ESP: {command}")

    # Certifique-se de que command seja uma string
    message = {
        "name": name,
        "command": str(command)
    }  # Converte o booleano para string ('True' ou 'False')

    bootstrap_servers = 'kafka_kafka1_1:19091'
    conf = {
        'bootstrap.servers': bootstrap_servers
    }

    print(f"Connecting to Kafka broker at {bootstrap_servers}")
    producer = Producer(conf)
    topic = 'command_esp'

    print(f"Producing message to topic {topic}")
    print("Message to be sent:", message)

    def delivery_report(err, msg):
        if err is not None:
            abort(500, description=f"Kafka error: {err.str()}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    try:
        print("Sending message to Kafka")
        producer.produce(topic, json.dumps(message).encode('utf-8'), callback=delivery_report)
        producer.flush()  # Aguarda até que a mensagem seja confirmada
    except Exception as e:
        abort(500, description=f"Error producing message: {str(e)}")

    return jsonify({"message": "Command sent to ESP", "command": command, "mcu": name})


@app.route("/main/dashboard", methods=["GET"])
def get_dashboard():
    try:
        number_mcus = Model.count_mcus()

        data = Model_dataweather.get_last()
        data = {
            "num_mcus": number_mcus,
            "temperature": round(data['main']['temp'] - 273.15, 2),  # Apenas o valor do último registro
            "humidity": data['main']['humidity'],  # Apenas o valor do último registro
            "wind_speed": data['wind']['speed'],  # Apenas o valor do último registro
            "timestamp": data['dt']  # Apenas o valor do timestamp
        }
        print(data)
        return json.loads(json_util.dumps(data))
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return jsonify({"message": "Erro ao buscar dados!"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

