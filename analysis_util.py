from collections import Counter
from globals import *
from video_utils import *


def doAnalysis(match_list, mismatch_list, tile_count, frame_count):
    match_counter = Counter(match_list)
    mismatch_counter = Counter(mismatch_list)
    return match_counter, mismatch_counter

def doAnalysis2(same,diff,R_faces,F_faces,frame_count):
    return



