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
    tqdm_value = frame_count
    progress_bar = tqdm(desc="Detecting Face", total=tqdm_value)

    mtcnn = MTCNN(margin=0,thresholds=[0.85, 0.95, 0.95])
    face_tiles = []
    row = -1
    col = -1
    failed_detection_count = 0
    for  i in range(0, frame_count):

        # Detect faces
        try:
            f = cv2.cvtColor(frames[i], cv2.COLOR_BGR2RGB)

            boxes, _ = mtcnn.detect(f)
            topX = boxes[0][0]
            topY = boxes[0][1]
            bottomX = boxes[0][2]
            bottomY = boxes[0][3]
            row = int(topY) + TILE_SIZE - int(topY) % TILE_SIZE
            col = int(topX) + TILE_SIZE - int(topX) % TILE_SIZE
            #print (f"X:{topX} C:{col} Y:{topY} R:{row}")
        except:
            print("*")
            failed_detection_count += 1
        progress_bar.update(1)


        face_tiles.append((i,row,col))

    return face_tiles, failed_detection_count


