import sys
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append("/Users/harshpreetsingh/Documents/minor-project/final_pipeline")
sys.dont_write_bytecode = True

from services.config_services import config
config_parser = config()
import warnings
warnings.filterwarnings("ignore")

from input_services.process_input import HandleData
import random

class ConsolidateData:

    def __init__(self) -> None:
        self.df = pd.DataFrame()
    
    def format(self):
        obj = HandleData()
        self.df = obj.heartData()
        self.df = obj.nonMLFlag()
        self.df.to_csv("temp.csv")
        ml_flag = []
        non_ml_flag = self.df['non_ml_flag']
        for i in range(len(non_ml_flag)):
            ml_flag.append(random.randint(0,2))

        # self.df['predicted_stress_label'] = ml_flag
        plt.plot(self.df['time_stamp'], ml_flag[:len(non_ml_flag)])
        plt.plot(self.df['time_stamp'], non_ml_flag[:len(ml_flag)])
        plt.legend(["ml_flag", "non_ml_flag"], loc ="upper right")
        plt.xlabel("time")
        plt.ylabel("predictions")
        plt.show()


if __name__ == "__main__":
    obj= ConsolidateData()
    obj.format()
    
    