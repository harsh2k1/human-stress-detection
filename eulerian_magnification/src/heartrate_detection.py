import cv2
import heartrate, eulerian, pyramids
import numpy as np

class ECG:

    def __init__(self, frame, video_frames, face_rects, faceCascade, fps) -> None:
        self.img = frame
        self.video_frames = video_frames
        self.face_rects = face_rects
        self.faceCascade = faceCascade
        self.fps = fps
        self.freq_min = 1
        self.freq_max = 1.8

    # @staticmethod
    def getHeartRate(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        roi_frame = self.img

        # Detect face
        if len(self.video_frames) == 0:
            self.face_rects = self.faceCascade.detectMultiScale(gray, 1.3, 5)

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
        # print("Heart rate: ", heart_rate, "bpm")
        return heart_rate, self.video_frames, self.face_rects
