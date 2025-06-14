# Cloud USP

Este é o projeto **Cloud USP**, que utiliza Kafka, Docker e Python para comunicação entre um produtor e um consumidor.

## Passos para configurar e executar o projeto:

### 1. Configurar o Ambiente Virtual
1. Navegue até o diretório `consumer`.
2. Crie um ambiente virtual com o comando:

   ```bash
   python -m venv venv 
Ative o ambiente virtual:

Windows:
   .\venv\Scripts\activate

Linux/Mac:
    source venv/bin/activate 


Instale as bibliotecas necessárias:
     pip install -r requirements.txt

### 2. Executar o Docker Compose
Nos seguintes diretórios, execute o comando abaixo para inicializar os serviços:

..\cloud\kafka\
..\cloud\producer\

No terminal, navegue até cada pasta e execute:

      docker-compose up

Além de fazer o build do consumer 

      docker build -t consumer_open_weather .
      
      docker run --name consumer_open_weather --network net-esp -p 9005:9005 -d consumer_open_weather


(subir o banco de dados)

      docker run --name mongo-esp --network net-esp -p 27017:27017 -d mongodb/mongodb-community-server:latest

### Explicação do Comando
--name mongo-esp: Nomeia o contêiner como mongo-esp.

--network net-esp: Executa o contêiner na rede interna chamada net-esp.

-p 27017:27017: Mapeia a porta 27017 do contêiner para a porta 27017 da sua máquina host. Isso permite acesso externo ao MongoDB via localhost:27017 ou ip_do_seu_pc:27017.
-d: Executa o contêiner em segundo plano.

mongo/mongodb-community-server:latest: A imagem do MongoDB a ser usada.

Acesso Interno e Externo

### Acesso Interno: 

Outros contêineres que estão na mesma rede net-esp podem acessar o MongoDB usando o nome do contêiner (mongo-esp).

### Acesso Externo: 

Você pode acessar o MongoDB a partir do seu computador ou scripts locais usando localhost:27017 ou ip_do_seu_pc:27017.

### 3. Executar o Consumer
Navegue até a pasta consumer.

Execute o script principal:

      python main.py

### Observações
Certifique-se de que o Docker está instalado e em execução na sua máquina.
O requirements.txt deve conter todas as bibliotecas necessárias para o consumidor.
