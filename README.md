
# 🌱 Cloud USP - Smart Irrigation System (IoT + Kafka + ESP32 + React)

This repository contains the Cloud USP - Smart Irrigation System, a comprehensive solution for precision agriculture that integrates multiple technologies across IoT, cloud infrastructure, and web development.

The project leverages a distributed architecture combining:

    IoT devices (ESP32 microcontrollers + DHT11 sensors) for real-time environmental data acquisition (temperature, humidity, etc.).

    MQTT (via Mosquitto Broker) for lightweight and efficient communication between field devices and the cloud.

    Apache Kafka for high-throughput, fault-tolerant, and scalable data streaming between backend services.

    MongoDB for flexible NoSQL data storage of both sensor data and external weather information.

    Python-based microservices, including a Kafka consumer that ingests data from the OpenWeather API, providing real-time weather forecasts.

    React-based Frontend (using the Mantis Admin Template) for intuitive visualization of environmental metrics and remote control of field devices (like irrigation pumps).

    Docker and Docker Compose for containerized deployment and orchestration of all backend services.

This architecture enables farmers and operators to monitor real-time field conditions, analyze weather patterns, and remotely control irrigation systems via a web interface — all with an emphasis on scalability, low-cost deployment, and efficient resource usage.

The system is especially tailored for smallholder farms in Brazil, providing an affordable, extensible, and easy-to-deploy smart agriculture solution.

---

## Overview

The system enables:

- Real-time monitoring of **environmental variables** (temperature, humidity, wind speed, etc).
- Integration of **OpenWeather API** forecasts with local sensor data.
- **Remote control** of irrigation devices.
- Visualization of data and charts in a **responsive web interface**.

---

## System Architecture
![System Architecture](./images/projeto_.png)


### Main Components:

- **ESP32:** Sensor data acquisition and actuator control.
- **MQTT (Mosquitto):** Communication between devices and backend.
- **Kafka:** Internal asynchronous messaging pipeline.
- **MongoDB:** Data persistence.
- **Backend (Python + Docker):** Message processing and database integration.
- **Frontend (React + Mantis Template):** Data visualization and device control UI.
- **OpenWeather API:** External weather data source.

---

## Example Screenshots

### Weather Data Visualization:

*Example:*  
![Weather Data Visualization](./images/dados_metoroloficos.PNG)

---

### Per-Device Monitoring:

*Example:*  

![Per-Device Monitoring](./images/dados-esp.PNG)

---

## Setup and Run Instructions

### 1. Set Up Python Virtual Environment

Navigate to the **consumer** directory:

```bash
cd consumer
python -m venv venv
```

Activate the virtual environment:

- **Windows:**
```bash
.env\Scriptsctivate
```
- **Linux/Mac:**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 2. Start Docker Containers (Kafka, MongoDB, etc.)

In the following directories:

- `..\cloud\kafka\`
- `..\cloud\producer\`

Run:

```bash
docker-compose up
```

---

### 3. Build and Run the Consumer (OpenWeather Consumer)

In the `consumer` directory:

```bash
docker build -t consumer_open_weather .
```

Run the container:

```bash
docker run --name consumer_open_weather --network net-esp -p 9005:9005 -d consumer_open_weather
```

---

### 4. Run MongoDB

```bash
docker run --name mongo-esp --network net-esp -p 27017:27017 -d mongodb/mongodb-community-server:latest
```

**Quick Explanation:**

- `--name mongo-esp`: Container name.
- `--network net-esp`: Internal Docker network.
- `-p 27017:27017`: Exposes MongoDB port.
- `mongodb/mongodb-community-server:latest`: MongoDB image.

---

### 5. Run the Consumer Manually (Optional)

```bash
cd consumer
python main.py
```

---

### 6. Deploy Backend / Frontend

- **Backend:** Run backend services (Node.js or Python) with access to Kafka and MongoDB.
- **Frontend:** React (Mantis Template) → Access via browser:

If running locally:

```
http://localhost:5082/
```

If deployed on USP server:

```
http://andromeda.lasdpc.icmc.usp.br:5082/
```

---

## ✅ Tested Functionalities

- Real-time data collection from ESP32 + MQTT.
- Kafka data pipeline.
- Data persistence in MongoDB.
- OpenWeather API integration.
- Real-time chart visualization via Frontend.
- Remote device control from web interface.

---

## 📂 Repository Structure

```plaintext
gcloudpos03/
├── Backend/
├── Frontend/
├── Firmware/
├── Docker/
├── Kafka/
├── MongoDB/
├── consumer/
├── docs/
│   └── img/
├── README.md
└── ...
```

---

## 📈 Results

- Real-time visualization of environmental variables.
- Remote irrigation control.
- Water waste reduction.
- Multi-ESP32 support.

---

## 🧪 Requirements

- **Docker + Docker Compose**
- **Python 3.x**
- **Node.js (for backend/frontend if applicable)**
- **ESP32 Board**
- **Running MQTT Broker**
- **Running Kafka + Zookeeper**
- **Running MongoDB**

---

## 📚 Technical References

- OpenWeather API
- Apache Kafka
- Mosquitto MQTT
- ESP32 Docs
- Mantis React Template (https://codedthemes.gitbook.io/mantis)

---

## ✅ Project Link

https://github.com/ICMC-SSC5973-2024/gcloudpos03

---

**Contributions are welcome!**  
Fork the project, open a PR, or report issues.
