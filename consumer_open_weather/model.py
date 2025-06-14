import pymongo
from dotenv import load_dotenv
import os
load_dotenv()  

class Model:
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.my_database = self.client[os.getenv("MONGO_DATABASE")]
        self.collection = self.my_database[os.getenv("MONGO_COLLECTION")]

    def insert(self, data):
        self.collection.insert_one(data)

    def get(self):
        return self.collection.find()

    def get_one(self, query):
        return self.collection.find_one(query)

    def update(self, query, data):
        self.collection.update_one(query, {"$set": data})

    def delete(self, query):
        self.collection.delete_one(query)

