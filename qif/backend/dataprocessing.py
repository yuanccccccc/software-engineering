import os
import json
import pandas as pd
from bs4 import BeautifulSoup

# 获取当前脚本文件所在路径
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(script_dir, "水质数据")
all_data = []

# 遍历“水质数据”下所有一级子文件夹（例如：2020-05）
for month_folder in os.listdir(root_dir):
    month_path = os.path.join(root_dir, month_folder)
    if os.path.isdir(month_path):
        for file in os.listdir(month_path):
            if file.endswith(".json"):
                json_path = os.path.join(month_path, file)
                print(f"正在处理: {json_path}")
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                        thead = data.get("thead", [])
                        tbody = data.get("tbody", [])

                        if not thead or not tbody:
                            print(f"跳过：thead或tbody为空 - {json_path}")
                            continue

                        # 清洗表头（去掉 HTML 标签）
                        clean_thead = [
                            BeautifulSoup(str(col), "html.parser").get_text()
                            for col in thead
                        ]

                        # 逐行处理数据
                        for row in tbody:
                            clean_row = [
                                BeautifulSoup(str(cell), "html.parser").get_text()
                                for cell in row
                            ]
                            if len(clean_row) == len(clean_thead):
                                # 提取日期信息
                                try:
                                    year, month = month_folder.split('-')
                                except ValueError:
                                    year, month = '', ''
                                date = file.replace('.json', '')

                                # 合并数据
                                record = dict(zip(clean_thead, clean_row))
                                record["年份"] = year
                                record["月份"] = month
                                record["日期"] = date
                                all_data.append(record)
                            else:
                                print(f"行长度与表头不一致，跳过：{json_path}")
                except Exception as e:
                    print(f"解析失败: {json_path}，错误信息: {e}")

# 写入 CSV 文件
if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv("water_history.csv", index=False, encoding='utf-8-sig')
    print("✅ 数据写入成功：all_water_quality.csv")
else:
    print("⚠️ 没有收集到任何数据")
