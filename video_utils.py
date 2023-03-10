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

def binaryHeat(frames, frame_number, row, col, isGood):
    tile = frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE]
    tile[:, :, 0] = 0
    if (isGood):
        tile[:, :, 1] = 0
        tile[:, :, 2] = 255
    else:
        tile[:, :, 1] = 255
        tile[:, :, 2] = 0

def heatTile(frames, frame_number, row, col, numFrames, numTileBroken):
    tile = frames[frame_number][row:row+TILE_SIZE, col:col+TILE_SIZE]

    damageFactor = numTileBroken/numFrames
    greenVal = 255 * (1-damageFactor)
    redVal = 255 * damageFactor

    tile[:, :, 0] = 0
    tile[:, :, 1] = greenVal
    tile[:, :, 2] = redVal


def addTileBorder(frames, frame_number, row, col, numFrames, numTileBroken, numTotalTiles):
    tile = frames[frame_number][row:row+TILE_SIZE, col:col+TILE_SIZE]

    damageFactor = int( numTileBroken/(numFrames*numTotalTiles))
    greenVal = 255 * (1-damageFactor)
    redVal = 255 * damageFactor

    tile[0:1, :, 0] = 0
    tile[0:1, :, 1] = greenVal
    tile[0:1, :, 2] = redVal

    tile[TILE_SIZE - 5:TILE_SIZE, :, 0] = 0
    tile[TILE_SIZE - 5:TILE_SIZE, :, 1] = greenVal
    tile[TILE_SIZE - 5:TILE_SIZE, :, 2] = redVal

    tile[:, 0:5, 0] = 0
    tile[:, 0:5, 1] = greenVal
    tile[:, 0:5, 2] = redVal

    tile[:, TILE_SIZE - 5:TILE_SIZE, 0] = 0
    tile[:, TILE_SIZE - 5:TILE_SIZE, 1] = greenVal
    tile[:, TILE_SIZE - 5:TILE_SIZE, 2] = redVal


def showVideoSideBySide(frames_list, title_list, frame_count):
    while True:
        for f in range(0, frame_count):
            for i in range( 0, len(frames_list)):
                cv2.imshow(title_list[i], frames_list[i][f])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.waitKey(0)