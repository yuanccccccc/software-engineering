from flask import Flask
from extensions import db, jwt  # 从 extensions 导入 db 和 jwt
from routes import auth, admin
from models import User
from flask_cors import CORS
from data_process.app import data_process_bp
from data_process.dataprocessing import fish_data
from ai.ai_routes import ai_bp  # 导入 AI 蓝图

app = Flask(__name__)
CORS(app)
app.config.from_object("config.Config")

db.init_app(app)  # 初始化 SQLAlchemy
jwt.init_app(app)  # 初始化 JWT

# 注册路由蓝图
app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(data_process_bp)  # 注册 dataprocess 的蓝图
app.register_blueprint(ai_bp)  # 注册 AI 蓝图

app.add_url_rule("/api/fish_data", view_func=fish_data)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 初始化数据库
        print("db.create")
        admin_user = User.query.filter_by(username="admin").first()
        if not admin_user:
            admin_user = User(username="admin", role="admin")
            admin_user.set_password("admin123")  # 设置默认管理员密码
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created: username=admin, password=admin123")

    print("debug")
    app.run(debug=True)
