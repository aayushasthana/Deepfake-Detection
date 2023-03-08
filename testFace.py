import os
import glob
import time
import torch
import cv2
from PIL import Image
import numpy as np
from globals import *


from tqdm.notebook import tqdm

# See github.com/timesler/facenet-pytorch:
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face
import ssl
import tqdm
from tqdm import tqdm
import platform


def read_video(video_name):

    frames = []
    video_name_path = BASE_PATH + DATA_PATH + FILE_PATH + video_name

    cap = cv2.VideoCapture(video_name_path)
    if not cap.isOpened():
        print("Error opening video file {}".format(video_name))
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    try:
        for i in range(0, count):
            ret, f = cap.read()
            frames.append(f)
    except Exception as e:
        print(str(e))
    frames_array = np.array(frames)
    cap.release()
    height = height - height % TILE_SIZE
    width = width - width % TILE_SIZE
    return count, width, height, fps, frames_array

if __name__ == '__main__':

    ssl._create_default_https_context = ssl._create_unverified_context
    print(platform.platform())
    print(torch.backends.mps.is_available())
    torch.device('mps')
    mtcnn = MTCNN(margin=0,thresholds=[0.85, 0.95, 0.95])
    #mtcnn = MTCNN(keep_all=True,margin=80)

    frame_count, w, h, fps, R_frames = read_video("wynotylpnm.mp4")


    for i, frame in enumerate(R_frames):
        print('\rTracking frame: {}'.format(i + 1), end='')

        # Detect faces
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes, _ = mtcnn.detect(frame)

            for box in boxes:

                cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 2)
                cv2.imshow("torch",frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except:
            print("failed to detect")
            pass
    cv2.waitKey(0)

    print('\nDone')
