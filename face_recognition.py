import numpy as np
import cv2
import json
import pickle

class FaceRecognition:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    def detect_face_and_crop(self, img, write_rectangle=False):
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected_faces = self.face_cascade.detectMultiScale(gray_img, 1.2, 2)
        detected_faces = sorted(detected_faces, key=lambda x: x[2])[::-1][:1]
        if len(detected_faces) < 1:
            return None, None
        face_x, face_y, face_w, face_h = detected_faces[0]
        if write_rectangle:
            cv2.rectangle(img, (face_x, face_y), (face_x+face_w, face_y+face_h), (255, 0, 0), int(img.shape[1]/240))
            return img, None
        return gray_img, gray_img[int(face_y):int(face_y+face_h), int(face_x):int(face_x+face_w)]

    def get_angle_and_distance(self, eye1, eye2, img):
        eyes = [eye1, eye2]
        eye_1 = tuple()
        eye_2 = tuple()
        index = 0
        for (eye_x, eye_y, eye_w, eye_h) in eyes:
            if index == 0:
                eye_1 = (eye_x, eye_y, eye_w, eye_h)
            elif index == 1:
                eye_2 = (eye_x, eye_y, eye_w, eye_h)
            index = index + 1
        
        if eye_1[0] < eye_2[0]:
            left_eye = eye_1
            right_eye = eye_2
        else:
            left_eye = eye_2
            right_eye = eye_1
        
        left_eye_center = (int(left_eye[0] + (left_eye[2] / 2)), int(left_eye[1] + (left_eye[3] / 2)))
        left_eye_center_x = left_eye_center[0]
        left_eye_center_y = left_eye_center[1]
        right_eye_center = (int(right_eye[0] + (right_eye[2]/2)), int(right_eye[1] + (right_eye[3]/2)))
        right_eye_center_x = right_eye_center[0]
        right_eye_center_y = right_eye_center[1]

        angle = np.degrees(np.arctan2(right_eye_center_y - left_eye_center_y, right_eye_center_x - left_eye_center_x))
        eyes_centers_distance = np.linalg.norm(np.array(left_eye_center) - np.array(right_eye_center))
        if angle > -29 and angle < 29 and img.shape[1]/eyes_centers_distance < 3.275:
            return angle, eyes_centers_distance, left_eye_center, right_eye_center
        return None, None, None, None

    def find_eyes_with_conditions(self, eyes, img):
        for i in range(len(eyes)-1):
            angle, distance, left_eye_center, right_eye_center = self.get_angle_and_distance(eyes[i], eyes[i+1], img)
            if angle != None and distance != None:
                return angle, left_eye_center, right_eye_center
        return None, None, None

    def detect_eyes_and_rotate(self, grayscale_img, face):
        eyes = self.eye_cascade.detectMultiScale(face, 1.05, 2)
        if len(eyes) < 2:
            return None
        eyes = list(filter(lambda x: face.shape[1] / x[2] < 6 and x[1] < face.shape[0] / 2, eyes))               
        image_copy = grayscale_img.copy()
        eyes = sorted(eyes, key=lambda x: x[2])[::-1]
        angle, left_eye_center, right_eye_center = self.find_eyes_with_conditions(eyes, image_copy)
        if angle is None:
          return None
        M = cv2.getRotationMatrix2D(((left_eye_center[0] + right_eye_center[0]) / 2, (left_eye_center[1] + right_eye_center[1]) / 2), angle, 1)
        img_to_rotate = grayscale_img.copy()
        source_img_rotated = cv2.warpAffine(img_to_rotate, M, (img_to_rotate.shape[1], img_to_rotate.shape[0]))
        return source_img_rotated

    def recognise(self, webcam_img):
        gray_webcam_image, detected_face = self.detect_face_and_crop(webcam_img)
        if detected_face is None:
            return None
        webcam_image_rotated = self.detect_eyes_and_rotate(gray_webcam_image, detected_face)
        if webcam_image_rotated is not None:
            _, detected_face = self.detect_face_and_crop(webcam_image_rotated)
        rows, cols = detected_face.shape
        mask = np.zeros_like(detected_face)
        ellipse_mask=cv2.ellipse(mask, center=(rows//2, cols//2), axes=(5*cols//13, rows//2), angle=0, startAngle=0, endAngle=360, color=(255, 255, 255), thickness=-1)
        invert_ellipse_mask = cv2.bitwise_not(ellipse_mask)
        img_after_mask = np.bitwise_or(detected_face, invert_ellipse_mask)
        equal_img = cv2.equalizeHist(img_after_mask)
        resized_face = cv2.resize(equal_img ,(120, 120))
        flattened_face = np.array([resized_face.flatten()])
        face_after_lda = self.lda_model.transform(flattened_face)
        preds = self.svm_model.predict_proba(face_after_lda)[0]
        max_pred_class_i = 0
        max_pred = 0
        for i in range(len(self.svm_model.classes_)):
            if preds[i] > max_pred:
                max_pred = preds[i]
                max_pred_class_i = i
        max_pred = round(max_pred * 100, 2)
        return self.get_name_by_label(str(max_pred_class_i)) if max_pred >= 30 else None

    def prepare_model(self):
        with open('lda_model.yml', 'rb') as f_lda:
            self.lda_model = pickle.load(f_lda)
        with open('svm_model.yml', 'rb') as f_svm:
            self.svm_model = pickle.load(f_svm)
        with open('label_names.json', 'r') as f_labels:
            self.labels_names = json.load(f_labels)
        
    def get_name_by_label(self, label):
        return self.labels_names[label]

    def get_names(self):
        return self.labels_names.values()
