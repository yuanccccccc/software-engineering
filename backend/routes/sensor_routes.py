from flask import Blueprint
from backend.controllers.sensor_controller import (
    upload_sensor_data, 
    get_all_sensors, 
    export_sensor_data
)

sensor_bp = Blueprint('sensor', __name__)


@sensor_bp.route('/upload', methods=['POST'])
def upload():
    return upload_sensor_data()


@sensor_bp.route('/', methods=['GET'])
def get_all():
    return get_all_sensors()


@sensor_bp.route('/export', methods=['GET'])
def export():
    return export_sensor_data()
