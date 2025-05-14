import os

# 获取项目根目录
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 数据库连接字符串，确保数据库文件存放在项目的根目录
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'users.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用事件系统
    JWT_SECRET_KEY = "your-secret-key"  # JWT 密钥
