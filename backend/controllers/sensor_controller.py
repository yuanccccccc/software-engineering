from flask import jsonify, send_file, request
import os
from werkzeug.utils import secure_filename
from app.models.sensor import Sensor
from app.utils.file_processor import FileProcessor
from config import Config
import pandas as pd


def allowed_file(filename):
    return FileProcessor.allowed_file(filename, Config.ALLOWED_EXTENSIONS)


def upload_sensor_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        file.save(upload_path)
        
        try:
            # 处理上传的文件
            sensor_data = FileProcessor.process_uploaded_file(upload_path)
            
            # 清空现有数据并插入新数据
            Sensor.delete_all()
            for data in sensor_data:
                Sensor.create(data)
            
            # 删除上传的文件
            os.remove(upload_path)
            
            return jsonify({
                'code': 200,
                'message': '数据上传成功',
                'data': sensor_data
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400


def get_all_sensors():
    try:
        sensors = Sensor.get_all()
        # 转换ObjectId为字符串
        for sensor in sensors:
            sensor['_id'] = str(sensor['_id'])
        return jsonify(sensors)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def export_sensor_data():
    try:
        sensors = Sensor.get_all()
        
        # 准备导出路径
        export_filename = 'sensor_export.xlsx'
        export_path = os.path.join(Config.UPLOAD_FOLDER, export_filename)
        
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)
        
        # 生成导出文件
        FileProcessor.generate_export_file(sensors, export_path)
        
        # 发送文件
        return send_file(
            export_path,
            as_attachment=True,
            attachment_filename=export_filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # 删除临时文件
        if os.path.exists(export_path):
            os.remove(export_path)