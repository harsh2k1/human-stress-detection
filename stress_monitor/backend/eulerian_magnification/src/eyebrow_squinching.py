import dlib
from scipy.spatial import distance as dist
import numpy as np
import cv2
import imutils
from imutils import face_utils

import os
import sys
sys.path.append("")
sys.dont_write_bytecode = True

from services.config_services import config
config_parser = config()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(config_parser['PATH']['project_path'] + "/models/shape_predictor_68_face_landmarks.dat")


class EyebrowDetection:

    def __init__(self, frame, points) -> None:
        self.frame = frame
        self.points = points
    
    def eyebrowDistance(self,leye,reye):
        # global points
        distq = dist.euclidean(leye,reye)
        self.points.append(int(distq))
        return distq

    @staticmethod
    def normalizeValues(points,disp):
        normalized_value = abs(disp - np.min(points))/abs(np.max(points) - np.min(points))
        stress_value = np.exp(-(normalized_value))
        # print(stress_value)
        if stress_value>=0.70:
            return stress_value,"high_stress"
        else:
            return stress_value,"low_stress"

    
    def detectEyebrowSquinching(self):
        stress_label = 'no_stress'
        frame = cv2.flip(self.frame,1)
        frame = imutils.resize(frame, width=500,height=500)
        
        
        (lBegin, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
        (rBegin, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]

        #preprocessing the image
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
        detections = detector(gray,0)
        for detection in detections:
            # emotion = emotion_finder(detection,gray)
            # cv2.putText(frame, emotion, (10,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            shape = predictor(frame,detection)
            shape = face_utils.shape_to_np(shape)
            
            leyebrow = shape[lBegin:lEnd]
            reyebrow = shape[rBegin:rEnd]
                
            reyebrowhull = cv2.convexHull(reyebrow)
            leyebrowhull = cv2.convexHull(leyebrow)

            cv2.drawContours(frame, [reyebrowhull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [leyebrowhull], -1, (0, 255, 0), 1)

            distq = self.eyebrowDistance(leyebrow[-1],reyebrow[0])
            stress_value,stress_label = self.normalizeValues(self.points,distq)
            cv2.putText(frame,f"label: {stress_label} stress level:{str(int(stress_value*100))}",(20,40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return self.points, frame, stress_label
