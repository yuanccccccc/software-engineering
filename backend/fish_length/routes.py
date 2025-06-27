# fish_length/routes.py
from flask import Blueprint, request, jsonify
from .predictor import predict

fish_length_bp = Blueprint('fish_length', __name__)

@fish_length_bp.route('/api/predict_length', methods=['POST'])
def predict_length():
    data = request.json
    try:
        species = data['Species']
        weight = float(data['Weight(g)'])
        height = float(data['Height(cm)'])
        width = float(data['Width(cm)'])
    except Exception:
        return jsonify({'error': '参数错误或缺失'}), 400

    result = predict(species, weight, height, width)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)
