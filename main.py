# This is a sample Python script.

from signature_utils import *
from video_utils import *
from encrypt_utils import *
import argparse
import time


TILE_SIZE = 8

def cli_options():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True,
                    help="path of the video name")
    ap.add_argument("-n","--number", required=True,
                    help="first n frames ")

    args = vars(ap.parse_args())

    return args


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    args = cli_options()

    video_name = args["video"]
    first_n_frames = int(args["number"])

    frame_count, w, h, fps, frames = read_video(video_name)
    print("Video:{} Frame_count:{} Width:{} Height:{} FPS:{}".format(video_name, frame_count, w, h, fps))
    title = video_name + "pre-processing"
    show_videos_from_frames(frames, title)

    row_count = int(w/TILE_SIZE)
    col_count = int(h/TILE_SIZE)
    for f in range(0,first_n_frames):
        start_time = time.time()
        for row in range(0,row_count):
            for col in range(0,col_count):
                AssignSignature_perTile(frames,f,row,col,f, row,col,)
        end_time = time.time()
        print("{}-{} seconds".format(f, end_time-start_time))

    title = video_name + "post-processing"
    show_videos_from_frames(frames,title)




