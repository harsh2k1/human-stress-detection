import pickle
import sys
import numpy as np
sys.path.append("/Users/harshpreetsingh/Documents/minor-project/final_pipeline")
sys.dont_write_bytecode = True

from services.config_services import config
config_parser = config()

def stressPredictor(y_test, model, scaler):
    y_test = list(map(lambda z: 0 if str(z) == "nan" or str(z) == "inf" else z, y_test))
    y_test = scaler.fit_transform(np.array(y_test).reshape(1,-1))

    return model.predict(y_test)
