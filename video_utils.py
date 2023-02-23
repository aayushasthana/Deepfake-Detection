import cv2
import matplotlib.pyplot as plt
import numpy as np

TILE_SIZE = 8

def read_video(video_name):
    frames = []
    cap = cv2.VideoCapture(video_name)
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

    cap.release()
    return count, width, height, fps, frames


def display_tile(frames, frame_number, row, col, title):
    plt.imshow(frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])
    plt.title(title + "-f#{} r#{} c#{}".format(frame_number, row, col))
    plt.show()


def dump_tile(frames, frame_number, row, col, title):
    print(title + "-f#{} r#{} c#{}".format(frame_number, row, col))
    print(frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])


def display_frame(frames, frame_number, title):
    plt.figure()
    plt.imshow(cv2.cvtColor(frames[frame_number], cv2.COLOR_BGR2RGB))
    plt.title(title + "-f#{}".format(frame_number))
    plt.show()

def show_videos_from_frames(frames, caption):
    for f in frames:
        cv2.imshow(caption, f)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

def show_frames_side_by_side(frame_number,f1,caption1, f2, caption2):

    f, ax = plt.subplots(2, sharex=True)
    plt.suptitle("f#{} {}  ".format(frame_number, f1.shape))
    ax[0].imshow(f1)
    ax[0].set_title(caption1)
    ax[1].imshow(f2)
    ax[1].set_title(caption2)

    plt.show()



