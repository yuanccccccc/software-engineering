import os
import pandas as pd
from flask import jsonify


def fish_data():
    # 获取 CSV 文件路径
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(
        base_dir, "..", "fish_data.csv"
    )  # 假设文件已迁移到 backend 根目录
    df = pd.read_csv(csv_path)

    # 返回所有行，转成 List[Dict]
    result = df.to_dict(orient="records")
    return jsonify(result)
