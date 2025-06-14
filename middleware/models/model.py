from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Dict, Any
from datetime import datetime, timedelta


class Model:
    def __init__(self, collection_name: str):
        try:
            self.client = MongoClient("mongodb://mongo-esp:27017/")
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
        self.db = self.client["weather"]
        self.collection: Collection = self.db[collection_name]

    def insert(self, data: Dict[str, Any]) -> Any:
        return  self.collection.insert_one(data).inserted_id
    
    def get(self) -> list:
        return list(self.collection.find({}).sort('_id', -1).limit(100))
    
    def get_last(self):

        return self.collection.find_one(sort=[("dt", -1)])
    
    def get_one(self, query: Dict[str, Any]) -> Dict[str, Any]:
        return self.collection.find_one(query)
    

    def update(self, query: Dict[str, Any], data: Dict[str, Any]) -> None:
        self.collection.update_one(query, {"$set": data})

    def delete(self, query: Dict[str, Any]) -> None:
        self.collection.delete_one(query)
        
    def get_recent(self, limit: int = 10) -> list:
        return list(self.collection.find({}).sort("_id", -1).limit(limit))
    
    def get_last_temperature_and_humidity(self, query: Dict[str, Any]) -> Dict[str, Any]:
        return self.collection.find_one(query, sort=[("timestamp", -1)])
    
    def get_lasts_temperature_and_humidity_by_name(self, name: str, limit: int = 30) -> list:
        return list(self.collection.find({"name": name}).sort("_id", -1).limit(limit))
    
    def count_mcus(self):
        # Conta o número de documentos com o campo 'name' (assumindo que 'name' é único para cada MCU)
        return self.collection.count_documents({"name": {"$exists": True}})
