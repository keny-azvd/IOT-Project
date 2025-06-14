
# 🌱 Cloud USP - Smart Irrigation System (IoT + Kafka + ESP32 + React)

Este é o repositório do **Cloud USP - Smart Irrigation System**, um projeto de **agricultura de precisão** que integra **IoT (ESP32 + sensores DHT11)**, **Cloud Computing**, **Kafka**, **MQTT**, **MongoDB**, **Python**, **React**, e **Docker**.

---

## 📌 Visão Geral

O sistema permite:

- Monitorar **variáveis ambientais em tempo real** (temperatura, umidade, vento, etc).
- Integrar previsões da **OpenWeather API** com dados locais.
- **Controlar remotamente** dispositivos de irrigação.
- Exibir dados e gráficos em uma **interface web responsiva**.

---

## 🧱 Arquitetura

```plaintext
[Sensores ESP32] → [Mosquitto MQTT Broker] → [Cloud Backend] → [Kafka] → [MongoDB] → [Frontend (React)]
                             ↑                                                    ↓
                    [Comandos via UI] ←-------------------------------------- [Usuário Web]
```

### Componentes principais:

- **ESP32:** Leitura de sensores e execução de comandos.
- **MQTT (Mosquitto):** Comunicação entre dispositivos e backend.
- **Kafka:** Pipeline de mensagens internas.
- **MongoDB:** Persistência de dados.
- **Backend (Python + Docker):** Processamento de mensagens e integração com o banco.
- **Frontend (React + Mantis Template):** Visualização de dados e controle dos dispositivos.
- **OpenWeather API:** Dados climáticos externos.

---

## 📷 Exemplos Visuais (Screenshots)

### 📊 Gráficos Meteorológicos:

*Exemplo:*  
![Gráfico Meteorológico](./docs/img/grafico_meteorologico.png)

---

### 🖥️ Controle de Atuadores:

*Exemplo:*  
![Controle de Atuadores](./docs/img/controle_atuadores.png)

---

### 📡 Monitoramento por Dispositivo:

*Exemplo:*  
![Visualização MCU](./docs/img/dados_mcus.png)

---

### 🔌 Circuito com ESP32:

*Exemplo:*  
![Circuito ESP32](./docs/img/circuito_esp32.png)

---

## 🛠️ Como Configurar e Rodar o Projeto

### 1. Configurar o Ambiente Virtual (Python)

Navegue até a pasta do **consumer**:

```bash
cd consumer
python -m venv venv
```

Ative o ambiente virtual:

- **Windows:**
```bash
.env\Scriptsctivate
```
- **Linux/Mac:**
```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

### 2. Subir os Containers Docker (Kafka, MongoDB, etc.)

Nos diretórios:

- `..\cloud\kafka\`
- `..\cloud\producer\`

Execute:

```bash
docker-compose up
```

---

### 3. Build e Rodar o Consumer (OpenWeather Consumer)

No diretório `consumer`:

```bash
docker build -t consumer_open_weather .
```

Execute o container:

```bash
docker run --name consumer_open_weather --network net-esp -p 9005:9005 -d consumer_open_weather
```

---

### 4. Subir o MongoDB

```bash
docker run --name mongo-esp --network net-esp -p 27017:27017 -d mongodb/mongodb-community-server:latest
```

**Explicação rápida:**

- `--name mongo-esp`: Nome do container.
- `--network net-esp`: Rede interna de containers.
- `-p 27017:27017`: Expõe a porta do MongoDB.
- `mongodb/mongodb-community-server:latest`: Imagem do MongoDB.

---

### 5. Executar o Consumer Manualmente (se preferir fora do Docker)

```bash
cd consumer
python main.py
```

---

### 6. Deploy do Backend / Frontend

- **Backend:** Rodar os serviços (ex: Node.js ou Python) com acesso ao Kafka e MongoDB.
- **Frontend:** React (Template Mantis) → acessar via navegador:

Se estiver local:

```
http://localhost:5082/
```

Se estiver no servidor da USP:

```
http://andromeda.lasdpc.icmc.usp.br:5082/
```

---

## ✅ Funcionalidades Testadas

- Coleta de dados em tempo real com ESP32 + MQTT.
- Pipeline de dados com Kafka.
- Persistência de dados no MongoDB.
- Integração com OpenWeather API.
- Visualização de gráficos via Frontend.
- Controle remoto de dispositivos de campo.

---

## 📂 Estrutura do Repositório

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

## 📈 Resultados

- Visualização em tempo real de variáveis ambientais.
- Controle remoto de irrigação.
- Redução de desperdício de água.
- Suporte a múltiplos ESP32 conectados.

---

## 🧪 Requisitos

- **Docker + Docker Compose**
- **Python 3.x**
- **Node.js (para backend/frontend se aplicável)**
- **Placa ESP32**
- **Broker MQTT ativo**
- **Kafka + Zookeeper ativos**
- **MongoDB ativo**

---

## 📚 Referências Técnicas

- OpenWeather API
- Apache Kafka
- Mosquitto MQTT
- ESP32 Docs
- Mantis React Template (https://codedthemes.gitbook.io/mantis)

---

## ✅ Link para o Projeto

https://github.com/ICMC-SSC5973-2024/gcloudpos03

---

**Contribuições são bem-vindas!**  
Faça um fork, abra um PR ou reporte issues.
