import cv2
import pyramids
import heartrate
from heartrate_detection import ECG
# import preprocessing
import eulerian
import numpy as np

import os
import sys
sys.path.append("/Users/harshpreetsingh/Documents/minor-project/final_pipeline")
sys.dont_write_bytecode = True

from services.config_services import config
config_parser = config()


# Frequency range for Fast-Fourier Transform
freq_min = 1
freq_max = 1.8

# Preprocessing phase
print("Reading + preprocessing video...")

faceCascade = cv2.CascadeClassifier(config_parser['PATH']['project_path'] + "/models/haarcascade_frontalface_alt0.xml")
cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS))
video_frames = []
face_rects = ()

class test:

    def __init__(self, frame, video_frames, face_rects, fps) -> None:
        self.img = frame
        self.video_frames = video_frames
        self.face_rects = face_rects
        # self.faceCascade = faceCascade
        self.fps = fps
        self.freq_min = 1
        self.freq_max = 1.8

    # @staticmethod
    def foo(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        roi_frame = self.img

        # Detect face
        if len(self.video_frames) == 0:
            self.face_rects = faceCascade.detectMultiScale(gray, 1.3, 5)

        # Select ROI
        if len(self.face_rects) > 0:
            for (x, y, w, h) in self.face_rects:
                roi_frame = self.img[y:y + h, x:x + w]
            if roi_frame.size != self.img.size:
                roi_frame = cv2.resize(roi_frame, (500, 500))
                frame = np.ndarray(shape=roi_frame.shape, dtype="float")
                frame[:] = roi_frame * (1. / 255)
                self.video_frames.append(frame)

        # Build Laplacian video pyramid
        lap_video = pyramids.build_video_pyramid(self.video_frames)

        amplified_video_pyramid = []
        heart_rate = 0
        for i, video in enumerate(lap_video):
            if i == 0 or i == len(lap_video)-1:
                continue

            # Eulerian magnification with temporal FFT filtering
            result, fft, frequencies = eulerian.fft_filter(video, self.freq_min, self.freq_max, self.fps)
            lap_video[i] += result

            # Calculate heart rate
            heart_rate = heartrate.find_heart_rate(fft, frequencies, self.freq_min, self.freq_max)

        # Output heart rate and final video
        print("Heart rate: ", heart_rate, "bpm")
        return heart_rate, self.video_frames, self.face_rects


while True:

    ret, img = cap.read()
    if not ret:
        break

    obj = test(frame=img, video_frames=video_frames, face_rects=face_rects, fps=fps)

    heart_rate, video_frames, face_rects = obj.foo()
    
    cv2.imshow("Frame", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break