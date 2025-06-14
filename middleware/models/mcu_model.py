from models.model import Model

class McuModel(Model):
    def __init__(self):
        super().__init__(collection_name="data_weather")
