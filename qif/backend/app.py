from flask import Flask, request, jsonify
from flask_cors import CORS
from data_loader import read_all_water_quality
from collections import Counter
import pandas as pd
from collections import defaultdict

from dateutil import parser

def parse_datetime_flexible(s):
    try:
        return parser.parse(s)
    except Exception:
        return pd.NaT


app = Flask(__name__)
CORS(app)  # 允许跨域

@app.route('/api/sankey')
def sankey_data():
    df = pd.read_csv("all_water_quality.csv") 
    # 仅保留关键字段 + 去除非法项
    df = df[~df["水质类别"].isin(["*", "-"])]
    df = df[["省份", "流域", "水质类别"]].dropna()

    links_raw = []

    for _, row in df.iterrows():
        links_raw.append((row["省份"], row["流域"]))
        links_raw.append((row["流域"], row["水质类别"]))

    # 聚合成计数
    link_counts = Counter(links_raw)
    links = [{"source": s, "target": t, "value": v} for (s, t), v in link_counts.items()]
    nodes = list({n for s, t in link_counts for n in (s, t)})

    return jsonify({
        "nodes": [{"name": name} for name in nodes],
        "links": links
    })

@app.route("/api/province_trend")
def province_top8_trend():
    df = pd.read_csv("all_water_quality.csv") 

    if df.empty or "监测时间" not in df.columns or "省份" not in df.columns:
        return jsonify([])

    df = df.dropna(subset=["省份", "监测时间"])
    df["监测时间"] = df["监测时间"].apply(parse_datetime_flexible)
    df = df.dropna(subset=["监测时间"])
    df["date"] = df["监测时间"].dt.strftime("%Y-%m-%d")

    # 选出总数前8名省份
    top8 = df.groupby("省份").size().sort_values(ascending=False).head(8).index.tolist()

    result = []
    for province in top8:
        df_p = df[df["省份"] == province]
        date_counts = df_p.groupby("date").size().reset_index(name="count")

        # 保证按时间排序
        date_counts = date_counts.sort_values("date")

        # 均匀抽样10个时间点（如果不足10个则保留全部）
        if len(date_counts) > 10:
            step = len(date_counts) // 10
            sampled = date_counts.iloc[::step][:10]
        else:
            sampled = date_counts

        result.append({
            "province": province,
            "dates": sampled["date"].tolist(),
            "counts": sampled["count"].tolist()
        })
    return jsonify(result)



@app.route("/api/province_total")
def province_total():
    df = pd.read_csv("all_water_quality.csv") 
    df = df.dropna(subset=["省份"])
    
    grouped = df.groupby("省份").size().reset_index(name="count")
    
    result = [{"name": row["省份"], "value": int(row["count"])} for _, row in grouped.iterrows()]
    return jsonify(result)

def pie_color_palette():
    return ['#1456FE', '#00CCFF', '#142AFE', '#1493FE', '#252448']

@app.route('/api/pie_data')
def pie_data():
    df = pd.read_csv("all_water_quality.csv") 
    df = df[df["水质类别"] != "*"]
    df = df[["省份", "流域", "水质类别"]].dropna()

    # 统计每个流域的出现次数
    basin_counts = df["流域"].value_counts()
    top3_basins = basin_counts.head(3).index.tolist()

    # 聚合每个流域下不同水质类别的数量
    result = []
    for i, basin in enumerate(top3_basins):
        subset = df[df["流域"] == basin]
        quality_counts = subset["水质类别"].value_counts()
        colors = pie_color_palette()
        pie_data = {
            "title": f"{basin}",
            "color": colors[i % len(colors)],
            "data": []
        }
        for j, (label, count) in enumerate(quality_counts.items()):
            pie_data["data"].append({
                "value": int(count),
                "name": label,
                "itemStyle": {
                    "color": colors[j % len(colors)]
                }
            })
        result.append(pie_data)

    return jsonify(result)



# 原来的 /api/water 接口也保留
@app.route('/api/water')
def water_data():
    df = pd.read_csv("all_water_quality.csv") 
    df = df.sort_values(by="监测时间")
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/pht')
def get_pht_data():
    df = pd.read_csv("all_water_quality.csv") 

    # 字段检查
    required_cols = ["水温(℃)", "pH(无量纲)", "省份", "断面名称"]
    if df.empty or not all(col in df.columns for col in required_cols):
        return jsonify({"points": [], "avg_temp": 0, "avg_ph": 0, "provinces": []})

    # 清洗数据
    df = df.dropna(subset=required_cols)
    df = df[(df["水温(℃)"] != "*") & (df["pH(无量纲)"] != "*")]
    df["水温(℃)"] = pd.to_numeric(df["水温(℃)"], errors="coerce")
    df["pH(无量纲)"] = pd.to_numeric(df["pH(无量纲)"], errors="coerce")
    df = df.dropna(subset=["水温(℃)", "pH(无量纲)"])

    # 获取所有省份供前端使用
    provinces = sorted(df["省份"].dropna().unique().tolist())

    # 如果有筛选条件，按省过滤
    province = request.args.get("province")
    if province:
        df = df[df["省份"] == province]

    # 按“断面名称”聚合（平均温度和pH）
    grouped = df.groupby("断面名称")[["水温(℃)", "pH(无量纲)"]].mean().reset_index()

    # 构造带断面名称的点数据
    points = []
    for _, row in grouped.iterrows():
        points.append({
            "value": [round(row["水温(℃)"], 2), round(row["pH(无量纲)"], 2)],
            "name": row["断面名称"]
        })

    # 计算整体均值
    avg_temp = round(df["水温(℃)"].mean(), 2) if not df.empty else 0
    avg_ph = round(df["pH(无量纲)"].mean(), 2) if not df.empty else 0

    return jsonify({
        "points": points,
        "avg_temp": avg_temp,
        "avg_ph": avg_ph,
        "provinces": provinces
    })

@app.route('/api/eight_radar')
def get_top8_radar():
    df = pd.read_csv("all_water_quality.csv")  # 替换为你的实际路径

    needed_columns = [
        "流域", "溶解氧(mg/L)", "电导率(μS/cm)", "浊度(NTU)",
        "高锰酸盐指数(mg/L)", "氨氮(mg/L)", "总磷(mg/L)", "总氮(mg/L)"
    ]
    df = df[needed_columns].dropna()

    # 强制转换为数值类型
    for col in needed_columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna()  # 再次去除因 coercion 产生的 NaN

    top8_basins = df["流域"].value_counts().head(8).index.tolist()

    color_list = ['#00CCFF', '#FF9F7F', '#37A2DA', '#32C5E9',
                  '#FFDB5C', '#9FE6B8', '#FF7171', '#8378EA']

    radar_data = []
    for i, basin in enumerate(top8_basins):
        basin_df = df[df["流域"] == basin]
        avg_vals = [round(val, 2) for val in basin_df[needed_columns[1:]].mean().tolist()]
        print(f"流域: {basin}, 平均值: {avg_vals}")

        radar_data.append({
            "title": basin,
            "position": [f"{(i % 4) * 25 + 10}%", f"{5 + (i // 4) * 50}%"],
            "center": [f"{(i % 4) * 25 + 15}%", f"{25 + (i // 4) * 50}%"],
            "indicator": [
                {"text": "溶解氧", "max": 10},
                {"text": "电导率", "max": 1500},
                {"text": "浊度", "max": 50},
                {"text": "高锰酸盐指数", "max": 10},
                {"text": "氨氮", "max": 2},
                {"text": "总磷", "max": 0.5},
                {"text": "总氮", "max": 5}
            ],
            "data": [ {
                "value": avg_vals,
                "name": "均值",
                "color": color_list[i % len(color_list)]
            }]
        })

    return jsonify(radar_data)



@app.route("/api/filter_options", methods=["GET"])
def get_filter_options():
    df = pd.read_csv("water_history.csv")
    dimensions = ["省份", "流域", "断面名称", "年份", "月份", "日期"]

    for key in dimensions:
        value = request.args.get(key)
        if value:
            df = df[df[key] == value]

    options = {
        dim: sorted(df[dim].dropna().unique().tolist())
        for dim in dimensions if dim in df.columns
    }
    return jsonify(options)


@app.route("/api/water_quality", methods=["GET"])
def get_filtered_data():
    df = pd.read_csv("water_history.csv")
    filter_keys = ["省份", "流域", "断面名称", "年份", "月份", "日期"]
    metric = request.args.get("metric")

    # ✅ 安全控制：仅允许合法字段（防止 SQL 注入/非法字段访问）
    allowed_metrics = [
        "溶解氧(mg/L)", "电导率(μS/cm)", "pH(无量纲)", "氨氮(mg/L)",
        "总磷(mg/L)", "总氮(mg/L)", "水温(℃)", "高锰酸盐指数(mg/L)", "浊度(NTU)"
    ]
    if metric not in allowed_metrics:
        return jsonify({"error": "Invalid metric"}), 400

    for key in filter_keys:
        value = request.args.get(key)
        if value:
            df = df[df[key] == value]

    df[metric] = pd.to_numeric(df[metric], errors='coerce')
    df = df.dropna(subset=[metric, "日期"])

    df = df[["日期", metric]]
    df = df.groupby("日期").mean().reset_index().sort_values("日期")

    return jsonify(df.to_dict(orient="records"))

@app.route('/api/section_status')
def section_status():
    df = pd.read_csv('all_water_quality.csv')
    province = request.args.get('省份')
    basin = request.args.get('流域')

    if province:
        df = df[df['省份'] == province]
    if basin:
        df = df[df['流域'] == basin]

    # 获取每个断面名称的最新记录
    df = df.sort_values('监测时间')  # 假设“监测时间”字段存在
    latest_df = df.groupby('断面名称').tail(1)[['断面名称', '站点情况']]

    return jsonify(latest_df.to_dict(orient='records'))

@app.route('/api/section_options')
def section_options():
    df = pd.read_csv('all_water_quality.csv')
    provinces = sorted(df['省份'].dropna().unique().tolist())
    basins = sorted(df['流域'].dropna().unique().tolist())
    return jsonify({'省份': provinces, '流域': basins})

if __name__ == '__main__':
    app.run(debug=True)
