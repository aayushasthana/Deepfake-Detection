
import pickle
import json
import argparse
from collections import Counter
from globals import *
from video_utils import *
from encrypt_utils import *
from signature_utils import *
from analysis_util import *

def getMetadata(jsonFile):
    json_filename = BASE_PATH + DATA_PATH + FILE_PATH + jsonFile
    print(f"JSON : {json_filename}")

    f = open(json_filename)
    # loading data
    data = json.load(f)
    dict_videos = {}
    count = 0

    for i in data:
        if (data[str(i)]["label"] == "FAKE"):
            dict_videos[count] = [str(i), data[str(i)]["original"]]
            count += 1

    f.close()

    return count ,dict_videos


def cli_options():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--count", required=False,
                    help="count of videos")
    ap.add_argument("-n", "--framecount", required=False,
                    help="frame count per video")
    ap.add_argument("-j", "--json", required=False,
                    help="json meta data file path")
    ap.add_argument("-t", "--test", required=False,
                    help="RR or RR' or RF or RF' or R'F' ")
    ap.add_argument("-r", "--results", required=False,
                    help="results file")

    args = vars(ap.parse_args())

    return args


if __name__ == '__main__':
    args = cli_options()
    count = int(args["count"])
    numFrames = int(args["framecount"])
    json_file = args["json"]
    testcase = args["test"]
    results = args["results"]

    publicKey, privateKey = get_keys()
    print(f"Testcase parameters: count:{count},framecount:{numFrames}, {testcase} {json_file} {results}")
    metadata_count, metadata_dict = getMetadata(json_file)
    for i in range(0, count):

        R = metadata_dict[int(i)][1]
        F = metadata_dict[int(i)][0]
        frames = []
        frame_count, w, h, fps, R_frames = read_video(R)
        frame_count, w, h, fps, F_frames = read_video(F)

        frame_count = numFrames

        if testcase == "F":
            matching, mismatch = checkSignature(F_frames, h, w, frame_count, publicKey, privateKey)
            print(f"Mismatch = {len(mismatch)}, Matching = {len(matching)}")

        elif testcase == "R":
            matching, mismatch = checkSignature(R_frames, h, w, frame_count, publicKey, privateKey)
            print(f"Mismatch = {len(mismatch)}, Matching = {len(matching)}")

        elif testcase == "R'":
            RPrime_frames = embedSignature(R_frames, h, w, frame_count, publicKey, privateKey)
            matching, mismatch = checkSignature(RPrime_frames, h, w, frame_count, publicKey, privateKey)
            print(f"Mismatch = {len(mismatch)}, Matching = {len(matching)}")

        elif testcase == "F'":
            RPrime_frames = embedSignature(R_frames, h, w, frame_count, publicKey, privateKey)
            matching, mismatch = checkSignature2(RPrime_frames, F_frames, h, w, frame_count, publicKey, privateKey)
            tileCount = int((h / TILE_SIZE) * (w / TILE_SIZE))
            print(f"Mismatch = {len(mismatch)}, Matching = {len(matching)}")

        elif testcase == "RR'" or testcase == "R'R":
            print(f"[{i}/{count}] RR' on {R}")
            RPrime_frames = embedSignature(R_frames, h, w, frame_count, publicKey, privateKey)
            # frame_count, w, h, fps, R_frames = read_video(R)  # this could be optimized
            matching, mismatch = compareSignature(R_frames, False, # encrypted
                                                  RPrime_frames, True, # encrypted
                                                  h, w, frame_count,
                                                  publicKey, privateKey)
        elif testcase == "RR":
            print(f"[{i}/{count}] RR on {R}")
            matching, mismatch = compareSignature(R_frames, False, # encrypted
                                                  R_frames, False, # encrypted
                                                  h, w, frame_count,
                                                  publicKey, privateKey)

        elif testcase == "RF" or testcase == "FR":
            print(f"[{i}/{count}] RF on {R} & {F}")
            matching, mismatch = compareSignature(R_frames, False, # encrypted
                                                  F_frames, False, # encrypted
                                                  h, w, frame_count,
                                                  publicKey, privateKey)

        elif testcase == "RF'" or testcase == "F'R":
            print(f"[{i}/{count}] RF' on {R} & {F}")
            FPrime_frames = embedSignature(F_frames, h, w, frame_count, publicKey, privateKey)
            matching, mismatch = compareSignature(R_frames, False, # encrypted
                                                  FPrime_frames, True, # encrypted
                                                  h, w, frame_count,
                                                  publicKey, privateKey)

        elif testcase == "R'F'" or testcase == "F'R'":
            print(f"[{i}/{count}] R'F' on {R} & {F}")
            RPrime_frames = embedSignature(R_frames, h, w, frame_count, publicKey, privateKey)
            FPrime_frames = embedSignature(F_frames, h, w, frame_count, publicKey, privateKey)
            matching, mismatch = compareSignature(RPrime_frames, True, # encrypted
                                                  FPrime_frames, True, # encrypted
                                                  h, w, frame_count,
                                                  publicKey, privateKey)

        match_counter, mismatch_counter = doAnalysis(matching, mismatch, int((h / TILE_SIZE) * (w / TILE_SIZE)),
                                                     frame_count)

        #Generating Regular Heat Map
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

        with open(results + "-" + str(i), 'wb') as fp:
            pickle.dump(matching, fp)
            pickle.dump(mismatch, fp)


