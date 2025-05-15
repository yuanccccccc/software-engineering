import os
import pandas as pd

def read_all_water_quality():
    base_path = os.path.join(os.path.dirname(__file__), "water_quality_by_name")
    records = []

    for province in os.listdir(base_path):
        province_path = os.path.join(base_path, province)
        if not os.path.isdir(province_path):
            continue

        for basin in os.listdir(province_path):
            basin_path = os.path.join(province_path, basin)
            for site in os.listdir(basin_path):
                site_path = os.path.join(basin_path, site)
                for date in os.listdir(site_path):
                    date_path = os.path.join(site_path, date)
                    for file in os.listdir(date_path):
                        if file.endswith(".csv"):
                            file_path = os.path.join(date_path, file)
                            try:
                                df = pd.read_csv(file_path, encoding='utf-8')
                                df["省份"] = province
                                df["流域"] = basin
                                df["断面"] = site
                                df["日期"] = date
                                records.append(df)
                            except Exception as e:
                                print(f"读取失败：{file_path} - {e}")

    if records:
        return pd.concat(records, ignore_index=True)
    else:
        return pd.DataFrame()
