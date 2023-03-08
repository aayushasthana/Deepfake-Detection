import cv2
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face

import tqdm
from tqdm import tqdm
import platform
from globals import *

def detectFaceHaarCascade(frames, frame_count):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # print(face_cascade)
    faces = []
    for i in range (0, frame_count):

        gray = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
        # print(gray)
        face = face_cascade.detectMultiScale(gray, 1.3, 10)
        print(face)
        faces.append(face)

    return faces

def detectFaceMTCNN(frames, frame_count):
    mtcnn = MTCNN(margin=0,thresholds=[0.85, 0.95, 0.95])
    face_tiles = []
    row = -1
    col = -1
    for  frame in range(0, frame_count):

        # Detect faces
        try:

            boxes, _ = mtcnn.detect(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            print(boxes)
            topX = boxes[0][0]
            topY = boxes[0][1]
            bottomX = boxes[0][2]
            bottomY = boxes[0][3]
            row = topX / TILE_SIZE
            col = topY / TILE_SIZE
        except:
            print("failed to detect")
        face_tiles.append((row,col))

    return face_tiles


