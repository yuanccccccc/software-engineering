from flask import Flask
from flask_pymongo import PyMongo
from config import Config

mongo = PyMongo()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    mongo.init_app(app)
    
    from backend.routes.sensor_routes import sensor_bp
    app.register_blueprint(sensor_bp, url_prefix='/api/sensor')
    
    return app
