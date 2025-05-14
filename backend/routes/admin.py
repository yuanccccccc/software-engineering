from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/", methods=["GET"])
@jwt_required()
def admin_dashboard():
    current_user = get_jwt_identity()
    if current_user["role"] != "admin":
        return jsonify({"message": "Access forbidden"}), 403
    return jsonify({"message": "Welcome, admin!"}), 200
