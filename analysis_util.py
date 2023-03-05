from collections import Counter
from globals import *
from video_utils import *


def doAnalysis(match_list, mismatch_list):
    match_counter = Counter(match_list)
    mismatch_counter = Counter(mismatch_list)
    return match_counter, mismatch_counter

'''
To be run in main after testcases:

#Generating Regular Heat Map
match_counter, mismatch_counter = doAnalysis(matching, mismatch)
topTiles = mismatch_counter.most_common(mismatch_counter.__sizeof__())
for j in range(0, frame_count):
    for k in range(0, len(topTiles)):
        heatTile(R_frames, j, topTiles[k][0][0], topTiles[k][0][1], numFrames, topTiles[k][1])

#Generating Pixel Heat Map
damage = pixelHeatMap(R_frames[0], F_frames[0])
for row in range(0, h):
    for col in range(0, w):
        heatTile2(F_frames, 0, row, col, damage[row][col])

showVideoSideBySide(R_frames, "F' Heat Map", F_frames, "Pixel Heat Map", frame_count)
'''