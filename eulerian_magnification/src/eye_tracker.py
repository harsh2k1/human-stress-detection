import cv2
import numpy as np
from face_detector import get_face_detector, find_faces
from face_landmarks import get_landmark_model, detect_marks

face_model = get_face_detector()
landmark_model = get_landmark_model()
left = [36, 37, 38, 39, 40, 41]
right = [42, 43, 44, 45, 46, 47]

cap = cv2.VideoCapture(0)
ret, img = cap.read()
thresh = img.copy()

cv2.namedWindow('image')
kernel = np.ones((9, 9), np.uint8)

def nothing(x):
    pass
cv2.createTrackbar('threshold', 'image', 75, 255, nothing)

class EyeTracker:

    def __init__(self, frame) -> None:
        self.frame = frame

    @staticmethod
    def eye_on_mask(mask, side, shape):
    
        points = [shape[i] for i in side]
        points = np.array(points, dtype=np.int32)
        mask = cv2.fillConvexPoly(mask, points, 255)
        l = points[0][0]
        t = (points[1][1]+points[2][1])//2
        r = points[3][0]
        b = (points[4][1]+points[5][1])//2
        return mask, [l, t, r, b]

    @staticmethod
    def find_eyeball_position(end_points, cx, cy):
        """Find and return the eyeball positions, i.e. left or right or top or normal"""
        x_ratio = (end_points[0] - cx)/(cx - end_points[2])
        y_ratio = (cy - end_points[1])/(end_points[3] - cy)
        if x_ratio > 3:
            return 1
        elif x_ratio < 0.33:
            return 2
        elif y_ratio < 0.33:
            return 3
        else:
            return 0

    def contouring(self,thresh, mid, img, end_points, right=False):
        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        try:
            cnt = max(cnts, key = cv2.contourArea)
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            if right:
                cx += mid
            cv2.circle(img, (cx, cy), 4, (0, 0, 255), 2)
            pos = self.find_eyeball_position(end_points, cx, cy)
            return pos
        except:
            pass

        return None

    
    @staticmethod
    def process_thresh(thresh):

        thresh = cv2.erode(thresh, None, iterations=2) 
        thresh = cv2.dilate(thresh, None, iterations=4) 
        thresh = cv2.medianBlur(thresh, 3) 
        thresh = cv2.bitwise_not(thresh)
        return thresh
    

    @staticmethod
    def print_eye_pos(img, left, right):
        text = ''
        if left == right and left != 0:
            
            if left == 1:
                # print('Looking left')
                text = 'eye_left'
            elif left == 2:
                # print('Looking right')
                text = 'eye_right'
            elif left == 3:
                # print('Looking up')
                text = 'looking_up'
            font = cv2.FONT_HERSHEY_SIMPLEX 
            cv2.putText(img, text, (20, 100), font,  0.5, (0, 255, 0), 2, cv2.LINE_AA) 
        
        return img, text


    def getEyePosition(self):
        img = self.frame
        rects = find_faces(img, face_model)
        text = ''
        
        for rect in rects:
            shape = detect_marks(img, landmark_model, rect)
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            mask, end_points_left = self.eye_on_mask(mask, left, shape)
            mask, end_points_right = self.eye_on_mask(mask, right, shape)
            mask = cv2.dilate(mask, kernel, 5)
            
            eyes = cv2.bitwise_and(img, img, mask=mask)
            mask = (eyes == [0, 0, 0]).all(axis=2)
            eyes[mask] = [255, 255, 255]
            mid = int((shape[42][0] + shape[39][0]) // 2)
            eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)
            threshold = cv2.getTrackbarPos('threshold', 'image')
            _, thresh = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
            thresh = self.process_thresh(thresh)
            
            eyeball_pos_left = self.contouring(thresh[:, 0:mid], mid, img, end_points_left)
            eyeball_pos_right = self.contouring(thresh[:, mid:], mid, img, end_points_right, True)
            
            img, text = self.print_eye_pos(img, eyeball_pos_left, eyeball_pos_right)

        return img, text