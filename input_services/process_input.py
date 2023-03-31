import json
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import pickle
sys.path.append("/Users/harshpreetsingh/Documents/minor-project/final_pipeline")
sys.dont_write_bytecode = True

from services.config_services import config
config_parser = config()

from src.make_predictions import stressPredictor
from src.extract_fields import FilterHeartData

with open(config_parser['PATH']['project_path']+"/models/prediction_rf_model.pkl","rb") as f:
    model = pickle.load(f)
    
scaler = pickle.load(open(config_parser['PATH']['project_path']+'/models/std_scaler.pkl','rb'))

class HandleData:
    
    def __init__(self) -> None:
        with open(config_parser['PATH']['project_path']+'/input_services/live_data.json','r') as f:
            self.raw_data = json.loads(f.read())
        self.df = pd.DataFrame(self.raw_data)
        self.df['time_stamp'] = pd.to_datetime(self.df['time_stamp'])
        self.df = self.df[self.df['heart_rate']>0]
        self.df['predicted_stress_label'] = [np.nan]*len(self.df)

    def heartData(self):
        heart_data = list(self.df['heart_rate'])
        iter = 0
        for _ in range(0,len(heart_data),5):
            
            obj = FilterHeartData(heart_data[iter:iter+5])
            y_test = obj.getAttributes()
            pred = stressPredictor(y_test, model=model, scaler=scaler)
            self.df['predicted_stress_label'][iter: iter+5] = pred[0]

            iter += 5
        
        return self.df
    
    def nonMLFlag(self):
        df = self.df.reset_index()
        df['non_ml_flag'] = [np.nan]*len(df)

        for i in range(len(df)):
            score = 0

            if df.loc[i,'eyebrow_flag'] == 'high_stress':
                score = 1

            if score and 'nan' not in str(df.loc[i,'eye_position_flag']):
                score = 2
            
            df['non_ml_flag'][i] = score
        
        self.df['non_ml_flag'] = df['non_ml_flag']

        return self.df



# obj = HandleData()
# obj.heartData()

# sample_data = [
#     {
#         "time_interval": "time",
#         "heart data": ""
#     }
# ]

# """
#     flags working:  # for 10s interval
        
#         flags:
#             1. eyebrow_squinch_interval
#             2. eye_blinks_pm
#             3. eye_contact_away_pm
#             4. head_position_away_pm

#         1. if eyebrow_squich_interval > threshold and eye_blinks_pm > normal, then high stress
#         2. if eye_contact_away_pm > threshold and head_position_away_pm > threshold, then moderate stress
#         3. if all four, then very high stress
# """