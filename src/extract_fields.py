import numpy as np
from scipy.stats import skew, kurtosis


class FilterHeartData:
    def __init__(self, hr_data) -> None:
        self.hr_data = np.array(hr_data)
        self.rr_intervals = []
        self.nn_intervals = []
        self.hr_power = (1/(1000*len(hr_data))) * np.abs(np.fft.fft(hr_data))**2
        self.sampling_rate = 1000
        self.time = np.arange(0, len(hr_data))

        self.mean_rr = np.nan
        self.median_rr = np.nan
        self.sdrr = np.nan
        self.rmssd = np.nan
        self.sdsd = np.nan
        self.pnn25 = np.nan
        self.pnn50 = np.nan
        self.kurt = np.nan
        self.skew = np.nan
        self.mean_rel_rr = np.nan
        self.median_rel_rr = np.nan
        self.stdd_rel_rr = np.nan
        self.rmssd_rel_rr = np.nan
        self.kurt_rel_rr = np.nan
        self.skew_rel_rr = np.nan
        self.vlf = np.nan
        self.lf = np.nan
        self.hf = np.nan
        self.lf_hf = np.nan
        self.hf_lf = np.nan


    def getRRIntervals(self):
        self.rr_intervals = np.array([60000/ele for ele in self.hr_data])

    def getNNIntervals(self):

        # Convert the data into a time series with a constant sampling rate of 1 Hz
        time = np.arange(0, len(self.hr_data))
        sampling_rate = 1

        # Find the indices of the normal beats
        normal_beats = np.where(self.hr_data >= 70)[0]

        # Calculate the NN intervals
        self.nn_intervals = time[normal_beats[1:]] - time[normal_beats[:-1]]

    def frequencyDomainConversion(self, lower_bound, upper_bound):

        # Find the indices of the frequency range
        indices = np.where((np.abs(self.hr_power) > lower_bound) & (np.abs(self.hr_power) < upper_bound))

        freq_component = np.sum(self.hr_power[indices])
        return freq_component

    
    def processIntervals(self):
        self.mean_rr = np.mean(self.rr_intervals)
        self.median_rr = np.median(self.rr_intervals)
        self.sdrr = np.std(self.rr_intervals)
        
        diffs = np.abs(self.nn_intervals[1:] - self.nn_intervals[:-1])
        self.rmssd = np.sqrt(np.mean(diffs**2))
        self.sdsd = np.std(diffs)

        pnn25_count = np.sum(np.abs(self.nn_intervals[1:] - self.nn_intervals[:-1]) > 0.025)
        self.pnn25 = pnn25_count / len(self.nn_intervals)
        pnn50_count = np.sum(np.abs(self.nn_intervals[1:] - self.nn_intervals[:-1]) > 0.05)
        self.pnn50 = pnn50_count / len(self.nn_intervals)

        self.kurt = kurtosis(self.rr_intervals)
        self.skew = skew(self.rr_intervals)

        rel_diffs = np.abs(self.nn_intervals[1:] - self.nn_intervals[:-1]) / self.nn_intervals[:-1]
        self.mean_rel_rr = np.mean(rel_diffs)
        self.median_rel_rr = np.median(rel_diffs)
        self.stdd_rel_rr = np.std(rel_diffs)
        self.rmssd_rel_rr = np.sqrt(np.mean(rel_diffs**2))
        self.kurt_rel_rr = kurtosis(rel_diffs)
        self.skew_rel_rr = skew(rel_diffs)

        self.vlf = self.frequencyDomainConversion(lower_bound=-10000, upper_bound=0.04)
        self.lf = self.frequencyDomainConversion(lower_bound=0.04, upper_bound=0.15)
        self.hf = self.frequencyDomainConversion(lower_bound=0.15, upper_bound=1000)
        self.lf_hf = self.lf/self.hf
        self.hf_lf = 1/self.lf_hf


    def getAttributes(self):
        self.getRRIntervals()
        self.getNNIntervals()
        self.processIntervals()

        y_test = [
            self.mean_rr, self.median_rr, self.sdrr, self.rmssd, self.sdsd, np.mean(self.hr_data) ,self.pnn25, self.pnn50,
            self.kurt, self.skew, self.mean_rel_rr, self.median_rel_rr, self.stdd_rel_rr, self.rmssd_rel_rr, self.kurt_rel_rr,
            self.skew_rel_rr, self.vlf, self.lf, self.hf, self.lf_hf, self.hf_lf
        ]

        return y_test
    
# import json
# with open("/Users/harshpreetsingh/Documents/minor-project/final_pipeline/input_services/live_data_new.json","r") as f:
#     data = json.loads(f.read())

# data2 = [num for num in data if num>0]

# print(FilterHeartData(data2).getAttributes())
