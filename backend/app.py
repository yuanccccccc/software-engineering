from flask import Flask, request, jsonify
from extensions import db, jwt  # 从 extensions 导入 db 和 jwt
from routes import auth, admin
from models import User
from flask_cors import CORS
from data_process.app import data_process_bp
from data_process.dataprocessing import fish_data
from fish_recognition import fish_recognizer  # 导入鱼类识别器
import os
from werkzeug.utils import secure_filename
from ai.ai_routes import ai_bp  # 导入 AI 蓝图

app = Flask(__name__)
CORS(app)
app.config.from_object("config.Config")

# 配置文件上传
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db.init_app(app)  # 初始化 SQLAlchemy
jwt.init_app(app)  # 初始化 JWT

# 注册路由蓝图
app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(data_process_bp)  # 注册 dataprocess 的蓝图
app.register_blueprint(ai_bp)  # 注册 AI 蓝图

app.add_url_rule("/api/fish_data", view_func=fish_data)


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/fish_recognition", methods=["POST"])
def fish_recognition():
    """鱼类图像识别API"""
    try:
        # 检查是否有文件上传
        if "file" not in request.files:
            return jsonify({"success": False, "error": "没有上传文件"}), 400

        file = request.files["file"]

        # 检查文件是否为空
        if file.filename == "":
            return jsonify({"success": False, "error": "没有选择文件"}), 400

        # 检查文件类型
        if not allowed_file(file.filename):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f'不支持的文件类型，支持的格式: {", ".join(ALLOWED_EXTENSIONS)}',
                    }
                ),
                400,
            )

        # 读取文件数据
        file_data = file.read()

        # 进行鱼类识别
        result = fish_recognizer.predict(file_data)

        if result["success"]:
            return jsonify(
                {
                    "success": True,
                    "data": {
                        "predicted_class": result["predicted_class"],
                        "confidence": round(
                            result["confidence"] * 100, 2
                        ),  # 转换为百分比
                        "top_3": [
                            {
                                "name": item["name"],
                                "confidence": round(item["confidence"] * 100, 2),
                            }
                            for item in result["top_3"]
                        ],
                    },
                }
            )
        else:
            return (
                jsonify({"success": False, "error": result.get("error", "识别失败")}),
                500,
            )

    except Exception as e:
        print(f"识别过程中发生错误: {str(e)}")
        return jsonify({"success": False, "error": f"服务器内部错误: {str(e)}"}), 500


@app.route("/api/fish_recognition/test", methods=["GET"])
def test_fish_recognition():
    """测试鱼类识别模型是否正常加载"""
    try:
        if fish_recognizer.model is None:
            return jsonify(
                {
                    "success": False,
                    "error": "模型未加载",
                    "model_path": fish_recognizer.model_path,
                }
            )
        else:
            return jsonify(
                {
                    "success": True,
                    "message": "模型加载正常",
                    "class_count": len(fish_recognizer.class_names),
                    "classes": fish_recognizer.class_names,
                }
            )
    except Exception as e:
        return jsonify({"success": False, "error": f"测试失败: {str(e)}"})


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
