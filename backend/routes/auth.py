from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import db  # 从 extensions 导入 db
from models import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
def register():
    data = request.json
    print("Received data:", data)
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "Username already exists"}), 400
    new_user = User(username=data["username"])
    new_user.set_password(data["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    print("Received data:", data)
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.check_password(data["password"]):
        token = create_access_token(
            identity={"username": user.username, "role": user.role}
        )
        return jsonify({"token": token, "role": user.role}), 200
    return jsonify({"message": "Invalid username or password"}), 401
