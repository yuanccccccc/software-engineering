# fish_length/predictor.py
import os
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, 'fish_model.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, 'species_encoder.pkl')
CSV_PATH = os.path.join(BASE_DIR, '..', 'data', 'fish_data.csv')

def train_model():
    df = pd.read_csv(CSV_PATH)
    le = LabelEncoder()
    df['Species_enc'] = le.fit_transform(df['Species'])

    features = ['Species_enc', 'Weight(g)', 'Height(cm)', 'Width(cm)']
    targets = ['Length1(cm)', 'Length2(cm)', 'Length3(cm)']

    X = df[features]
    y = df[targets]

    model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)
    print("模型训练并保存完成")

# 加载或训练模型
if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
    train_model()

model = joblib.load(MODEL_PATH)
le = joblib.load(ENCODER_PATH)

def predict(species, weight, height, width):
    if species not in le.classes_:
        return {"error": f"未知鱼种: {species}"}
    species_enc = le.transform([species])[0]
    X_pred = [[species_enc, weight, height, width]]
    y_pred = model.predict(X_pred)[0]
    return {
        'Length1(cm)': round(float(y_pred[0]), 3),
        'Length2(cm)': round(float(y_pred[1]), 3),
        'Length3(cm)': round(float(y_pred[2]), 3),
    }
