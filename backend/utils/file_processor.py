import pandas as pd
import os


class FileProcessor:
    @staticmethod
    def allowed_file(filename, allowed_extensions):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def process_uploaded_file(filepath):
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath)
        elif filepath.endswith('.json'):
            df = pd.read_json(filepath)
        else:
            raise ValueError("Unsupported file format")
        
        # 转换列名（支持中英文）
        column_mapping = {
            '设备名称': 'name',
            'name': 'name',
            '编号': 'id',
            'id': 'id',
            '类型': 'type',
            'type': 'type',
            '大小': 'size',
            'size': 'size',
            '状态': 'status',
            'status': 'status'
        }
        
        df.rename(columns=column_mapping, inplace=True)
        
        # 转换状态为英文
        status_mapping = {
            '正常': 'normal',
            '警告': 'warning',
            '故障': 'error',
            'normal': 'normal',
            'warning': 'warning',
            'error': 'error'
        }
        
        if 'status' in df.columns:
            df['status'] = df['status'].map(status_mapping)
        else:
            df['status'] = 'normal'
        
        return df.to_dict('records')
    
    @staticmethod
    def generate_export_file(sensors, output_path):
        df = pd.DataFrame(sensors)
        
        # 转换状态为中文
        status_mapping = {
            'normal': '正常',
            'warning': '警告',
            'error': '故障'
        }
        
        df['status'] = df['status'].map(status_mapping)
        
        # 重命名列名为中文
        df.rename(columns={
            'name': '设备名称',
            'id': '编号',
            'type': '类型',
            'size': '大小',
            'status': '状态'
        }, inplace=True)
        
        df.to_excel(output_path, index=False)
        return output_path