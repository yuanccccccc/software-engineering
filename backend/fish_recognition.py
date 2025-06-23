import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os

class FishRecognizer:
    def __init__(self, model_path='resnet50_model.h5'):
        """初始化鱼类识别器"""
        self.model_path = model_path
        self.model = None
        self.class_names = [
            '墨鱼', '多宝鱼', '带鱼', '石斑鱼', '秋刀鱼', '章鱼', '红鱼', '罗非鱼', 
            '胖头鱼', '草鱼', '银鱼', '青鱼', '马头鱼', '鱿鱼', '鲇鱼', '鲈鱼', 
            '鲍鱼', '鲑鱼', '鲢鱼', '鲤鱼', '鲫鱼', '鲳鱼', '鲷鱼', '鲽鱼', 
            '鳊鱼', '鳗鱼', '黄鱼', '黄鳝', '黑鱼', '龙头鱼'
        ]
        self.load_model()
    
    def load_model(self):
        """加载训练好的模型"""
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                print(f"模型加载成功: {self.model_path}")
            else:
                raise FileNotFoundError(f"模型文件不存在: {self.model_path}")
        except Exception as e:
            print(f"模型加载失败: {str(e)}")
            self.model = None
    
    def preprocess_image(self, image_data):
        """预处理图像数据"""
        try:
            # 如果输入是字节流，转换为PIL Image
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                image = image_data
            
            # 转换为RGB模式（如果是RGBA或其他模式）
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # 转换为numpy数组
            image_array = np.array(image)
            
            # 调整大小到224x224
            image_tensor = tf.image.resize(image_array, [224, 224])
            
            # 转换数据类型并归一化
            image_tensor = tf.cast(image_tensor, tf.float32)
            image_tensor = image_tensor / 255.0
            
            # 增加batch维度
            image_tensor = tf.expand_dims(image_tensor, axis=0)
            
            return image_tensor
        except Exception as e:
            print(f"图像预处理失败: {str(e)}")
            return None
    
    def predict(self, image_data):
        """预测鱼类"""
        if self.model is None:
            return {"success": False, "error": "模型未加载"}
        
        try:
            # 预处理图像
            processed_image = self.preprocess_image(image_data)
            if processed_image is None:
                return {"success": False, "error": "图像预处理失败"}
            
            # 进行预测
            predictions = self.model.predict(processed_image, verbose=0)
            
            # 获取预测结果
            pred_id = int(np.argmax(predictions))
            confidence = float(np.max(predictions))
            pred_name = self.class_names[pred_id]
            
            # 获取前3个预测结果
            top_3_indices = np.argsort(predictions[0])[-3:][::-1]
            top_3_results = []
            for idx in top_3_indices:
                top_3_results.append({
                    "name": self.class_names[idx],
                    "confidence": float(predictions[0][idx])
                })
            
            return {
                "success": True,
                "predicted_class": pred_name,
                "predicted_id": pred_id,
                "confidence": confidence,
                "top_3": top_3_results
            }
        except Exception as e:
            print(f"预测失败: {str(e)}")
            return {"success": False, "error": f"预测失败: {str(e)}"}

# 全局实例
fish_recognizer = FishRecognizer()