import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取项目根目录
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # -------------------------------
    # 数据库配置
    # -------------------------------
    
    # SQLite 配置（原配置）
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, 'users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用事件系统
    
    # MongoDB 配置（新增配置）
    MONGO_URI = os.getenv('MONGO_URI', 
                          'mongodb://localhost:27017/sensor_dashboard')
    MONGO_DB_NAME = 'sensor_dashboard'  # 默认数据库名
    
    # -------------------------------
    # 安全与认证配置
    # -------------------------------
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # 从环境变量读取
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-flask-secret')
    
    # -------------------------------
    # 文件上传配置
    # -------------------------------
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv', 'json'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB 文件大小限制
    
    # -------------------------------
    # 应用基础配置
    # -------------------------------
    DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))
    
    # -------------------------------
    # 跨域配置
    # -------------------------------
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')  # 用逗号分隔的允许域名