import cv2
import pyramids
import heartrate
from heartrate_detection import ECG
from eyebrow_squinching import EyebrowDetection
from head_pos_estimation import HeadPositionEstimation
from eye_tracker import EyeTracker
from blink_detection import DetectBlink
import eulerian
import numpy as np
from datetime import datetime
import json

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-s","--store",help="Store data?", default=0)
args = vars(parser.parse_args())

import os
import sys
sys.path.append("/Users/harshpreetsingh/Documents/minor-project/final_pipeline")
sys.dont_write_bytecode = True

from services.config_services import config
config_parser = config()

faceCascade = cv2.CascadeClassifier(config_parser['PATH']['project_path'] + "/models/haarcascade_frontalface_alt0.xml")
cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS))
video_frames = []
face_rects = ()
points = []
counter = 0
total = 0

data = []


while True:

    ret, img = cap.read()
    ori_img = img
    if not ret:
        break
    
    # heart rate flag
    hr_obj = ECG(frame=img, video_frames=video_frames, face_rects=face_rects, faceCascade=faceCascade, fps=fps)
    heart_rate, video_frames, face_rects = hr_obj.getHeartRate()

    # eyebrow flag
    eb_obj = EyebrowDetection(frame=img, points=points)
    points, img, stress_label = eb_obj.detectEyebrowSquinching()

    # head position flag
    hp_obj = HeadPositionEstimation(frame=img)
    img, head_position = hp_obj.getHeadPos()

    # eye position flag
    eye_obj = EyeTracker(frame=img)
    img, eye_position = eye_obj.getEyePosition()
    
    
    # # number of blinks flag
    blink_obj = DetectBlink(frame=img, counter=counter, total=total)
    _, counter, total = blink_obj.getNumberOfBlinks()


    # storing data
    # data.append({
    #     "time_stamp":str(datetime.now()),
    #     "heart_rate":heart_rate,
    #     "eyebrow_flag": stress_label,
    #     "head_position_flag": head_position,
    #     "eye_position_flag": eye_position
    # })
    data.append(heart_rate)
    

    cv2.putText(img,f"Heart Rate: {heart_rate} bpm",(20,60),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # cv2.putText(img, "Blinks: {}".format(total), (400, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Frame", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
        

cv2.destroyAllWindows()
cap.release()

if args['store']:
    with open("/Users/harshpreetsingh/Documents/minor-project/final_pipeline/input_services/live_data_new.json","w") as f:
        f.write(json.dumps(data))