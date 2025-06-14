# Cloud USP

This is the **Cloud USP** project, which uses Kafka, Docker, and Python for communication between a producer and a consumer.

## Steps to Set Up and Run the Project:

### 1. Set Up the Virtual Environment
1. Navigate to the `consumer` directory.
2. Create a virtual environment with the following command:

   ```bash
   python -m venv venv


Activate the virtual environment:

Windows:
   .\venv\Scripts\activate

Linux/Mac:
    source venv/bin/activate 

Install the required libraries:
     pip install -r requirements.txt

### 2. Run Docker Compose
In the following directories, run the command below to initialize the services:

..\cloud\kafka\
..\cloud\producer\

In the terminal, navigate to each folder and run:

      docker-compose up

Additionally, build the consumer:

      docker build -t consumer_open_weather .

Then, run it with:
      
      docker run --name consumer_open_weather --network net-esp -p 9005:9005 -d consumer_open_weather


(To start the database)

      docker run --name mongo-esp --network net-esp -p 27017:27017 -d mongodb/mongodb-community-server:latest

### Explanation of the Command
--name mongo-esp: Names the container as mongo-esp.

--network net-esp: Runs the container on the internal network called net-esp.

-p 27017:27017: Maps the container's port 27017 to port 27017 on your host machine. This allows external access to MongoDB via localhost:27017 or ip_of_your_pc:27017.

mongo/mongodb-community-server:latest: Specifies the MongoDB image to use.

Acesso Interno e Externo

### Internal Access:

Other containers on the same net-esp network can access MongoDB using the container's name (mongo-esp).

### External Access:

You can access MongoDB from your computer or local scripts using localhost:27017 or ip_of_your_pc:27017.

### 3. Run the Consumer

Navigate to the consumer folder.

Run the main script:

      python main.py

### Notes

    Make sure Docker is installed and running on your machine.

    The requirements.txt should contain all the necessary libraries for the consumer.
