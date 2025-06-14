from consumer import ConsumerWeather

class Main:
    def __init__(self):
        self.consumer = ConsumerWeather()

    def run(self):
        self.consumer.consume_data()

if __name__ == "__main__":
    main = Main()
    main.run()