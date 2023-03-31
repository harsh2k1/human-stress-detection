from scipy.spatial import distance as dist
import dlib
import sys
import cv2
from imutils import face_utils
sys.path.append("/Users/harshpreetsingh/Documents/minor-project/final_pipeline")
sys.dont_write_bytecode = True

from services.config_services import config
config_parser = config()

ar_thresh = 0.3
eye_ar_consec_frame = 5
counter = 0
total = 0

# get the frontal face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(config_parser['PATH']['project_path'] + "/models/shape_predictor_68_face_landmarks.dat")

class DetectBlink:

    def __init__(self, frame, counter, total) -> None:
        self.frame = frame
        self.counter = counter
        self.total = total

    @staticmethod
    def eye_aspect_ratio(eye):
        # compute the euclidean distances between the vertical landamrks
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        eye_opening_ratio = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return eye_opening_ratio

    def getNumberOfBlinks(self):
        (lBegin, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rBegin, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        #preprocessing the image
        gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        clahe_image = clahe.apply(gray)
        detections = detector(clahe_image,0)
        for detection in detections:
            shape = predictor(gray,detection)
            shape = face_utils.shape_to_np(shape)
            left_eye = shape[lBegin:lEnd]
            right_eye = shape[rBegin:rEnd]

            leftEyeHull = cv2.convexHull(left_eye)
            rightEyeHull= cv2.convexHull(right_eye)
            cv2.drawContours(clahe_image, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(clahe_image, [rightEyeHull], -1, (0, 255, 0), 1)
            #calculating the EAR
            left_eye_Ear = self.eye_aspect_ratio(left_eye)
            right_eye_Ear = self.eye_aspect_ratio(right_eye)

            avg_Ear = (left_eye_Ear + right_eye_Ear)/2.0

            if avg_Ear<ar_thresh:
                self.counter+=1
            else:
                if self.counter>eye_ar_consec_frame:
                    self.total+= 1
                self.counter = 0	
            cv2.putText(clahe_image, "Blinks: {}".format(self.total), (400, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return clahe_image, self.counter, self.total
