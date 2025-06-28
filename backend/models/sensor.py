from datetime import datetime
from backend import mongo


class Sensor:
    @staticmethod
    def get_collection():
        return mongo.db.sensors
    
    @staticmethod
    def create(data):
        data['created_at'] = datetime.utcnow()
        return Sensor.get_collection().insert_one(data)
    
    @staticmethod
    def delete_all():
        return Sensor.get_collection().delete_many({})
    
    @staticmethod
    def get_all():
        return list(Sensor.get_collection().find().sort('created_at', -1))
