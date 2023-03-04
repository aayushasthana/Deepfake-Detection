import cv2
import numpy as np
from globals import *


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


def heatTile(frames, frame_number, row, col, numFrames, numTileBroken):
    tile = frames[frame_number][row:row+TILE_SIZE, col:col+TILE_SIZE]

    damageFactor = numTileBroken/numFrames
    greenVal = 255 * (1-damageFactor)
    redVal = 255 * damageFactor

    tile[:, :, 0] = 0
    tile[:, :, 1] = greenVal
    tile[:, :, 2] = redVal


def heatTile2(frames, frame_number, row, col, damageFactor):
    tile = frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE]

    greenVal = 255 * (1 - damageFactor)
    redVal = 255 * damageFactor

    tile[:, :, 0] = 0
    tile[:, :, 1] = greenVal
    tile[:, :, 2] = redVal


def pixelHeatMap(framesA, framesB):
    framesC = np.abs(np.subtract(framesA, framesB))
    framesCR = framesC[:, :, 0]
    framesCG = framesC[:, :, 1]
    framesCB = framesC[:, :, 2]
    damageMap = (framesCR + framesCB + framesCG)/(255*3)
    return damageMap


def addTileBorder(frames, frame_number, row, col, numFrames, numTileBroken):
    tile = frames[frame_number][row:row+TILE_SIZE, col:col+TILE_SIZE]

    damageFactor = numTileBroken/numFrames
    greenVal = 255 * (1-damageFactor)
    redVal = 255 * damageFactor

    tile[0:5, :, 0] = 0
    tile[0:5, :, 1] = greenVal
    tile[0:5, :, 2] = redVal

    tile[TILE_SIZE - 5:TILE_SIZE, :, 0] = 0
    tile[TILE_SIZE - 5:TILE_SIZE, :, 1] = greenVal
    tile[TILE_SIZE - 5:TILE_SIZE, :, 2] = redVal

    tile[:, 0:5, 0] = 0
    tile[:, 0:5, 1] = greenVal
    tile[:, 0:5, 2] = redVal

    tile[:, TILE_SIZE - 5:TILE_SIZE, 0] = 0
    tile[:, TILE_SIZE - 5:TILE_SIZE, 1] = greenVal
    tile[:, TILE_SIZE - 5:TILE_SIZE, 2] = redVal


def showVideoSideBySide(framesA, titleA, framesB, titleB, count):
    while True:
        for f in range(0, count):
            cv2.imshow(titleA, framesA[f])
            cv2.imshow(titleB, framesB[f])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.waitKey(0)