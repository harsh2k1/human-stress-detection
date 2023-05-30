import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle
from backend.processing import statistical_features
from backend import read_config
config = read_config()

with open('backend/'+config['TRAINING']['model.base.dir']+'/hr_rf_model.pkl', 'rb') as f:
    model = pickle.load(f)


def predict_stress_level(data: list):
    data_dict = {}
    data_dict['HRR_Min'], data_dict['HRR_Max'], data_dict['HRR_Mean'], data_dict[
        'HRR_Std'], data_dict['HRR_RMS'] = statistical_features(data)
    data = pd.DataFrame([data_dict])

    scalar = MinMaxScaler()
    x_scaled = scalar.fit_transform(data)
    data = pd.DataFrame(x_scaled)
    data = data.fillna(0)

    pred_t = model.predict(data)

    return pred_t[0]
