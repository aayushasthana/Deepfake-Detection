import pickle
import json
import argparse
import time
from collections import Counter

import numpy as np

from globals import *
from video_utils import *
from encrypt_utils import *
from signature_utils import *
from analysis_util import *
from facenet_pytorch import MTCNN, InceptionResnetV1, extract_face
import ssl
import platform
import torch
from face_detect import *

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
    #-------- Code to enable Face detection using MTCNN --------
    #-------- look at enabling M1 support ----------------------
    ssl._create_default_https_context = ssl._create_unverified_context
    mps = torch.backends.mps.is_available()
    print(f" Platform {platform.platform()} M1: {mps}")
    if mps :
        torch.device('mps')
    else:
        torch.device('cpu')
    #-----------------------------------------------------------

    print(f"Testcase parameters: count:{count},framecount:{numFrames}, {testcase} {json_file} {results}")
    metadata_count, metadata_dict = getMetadata(json_file)
    if count == -1:
        count = metadata_count
    print(f"Metadata Count = {metadata_count}, Count = {count}")

    f = open("ExperimentResults/" + results + "0.txt", "a")
    f.write("RealVideoName,FakeVideoName,TotalFrames,TotalTiles,RuntimeRPrime,RuntimeFPrime,MismatchingTilesRPrime,MatchingTilesRPrime,MismatchingTilesFPrime,MatchingTilesFPrime\n")
    for i in range(0, count):
        if i % 100 == 0 and i != 0:
            f.close()
            print(str(int(i/100)) + "done")
            f = open("ExperimentResults/" + results + str(int(i/100)) + ".txt", "a")
            f.write("RealVideoName,FakeVideoName,TotalFrames,TotalTiles,RuntimeRPrime,RuntimeFPrime,MismatchingTilesRPrime,MatchingTilesRPrime,MismatchingTilesFPrime,MatchingTilesFPrime\n")

        startTime = time.time()
        R = metadata_dict[int(i)][1]
        F = metadata_dict[int(i)][0]
        frames = []
        frame_count, w, h, fps, R_frames = read_video(R)
        frame_count, w, h, fps, F_frames = read_video(F)

        if numFrames != -1:
            frame_count = numFrames
        # checking only for face tiles

        if testcase == "face":
            print(f"Video name : {R}")
            RPrime_frames = embedSignature(R_frames, h, w, frame_count, publicKey, privateKey)
            # Detect faces tile
            startRPrime = time.time()
            faceTiles = detectFaceMTCNN(R_frames,frame_count)
            print(faceTiles)
            #matchingF, mismatchF = checkSignature3(RPrime_frames, F_frames, h, w, faceTiles, 4, 4, frame_count, publicKey, privateKey)
            runtimeRPrime = time.time() - startRPrime

            print(f"Mismatch = {len(mismatchF)}, Matching = {len(matchingF)}")


        if testcase == "E":
            RPrime_frames = embedSignature(R_frames, h, w, frame_count, publicKey, privateKey)

            #R'
            startRPrime = time.time()
            matchingRPrime, mismatchRPrime = checkSignature(RPrime_frames, h, w, frame_count, publicKey, privateKey)
            runtimeRPrime = time.time() - startRPrime

            #F'
            startFPrime = time.time()
            matchingFPrime, mismatchFPrime = checkSignature2(RPrime_frames, F_frames, h, w, frame_count, publicKey, privateKey)
            runtimeFPrime = time.time() - startFPrime

        elif testcase == "F":
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

        #compute avg % percent diff in rgb across all frames



        #values for write
        realVideoName = metadata_dict[i][1];
        fakeVideoName = metadata_dict[i][0];
        totalFrames = frame_count;
        totalTiles = int((h / TILE_SIZE) * (w / TILE_SIZE)) * totalFrames
        #f.write("RealVideoName,FakeVideoName,TotalFrames,TotalTiles,RuntimeRPrime,RuntimeFPrime,MismatchingTilesRPrime,MatchingTilesRPrime,MismatchingTilesFPrime,MatchingTilesFPrime")
        #f.write(f"{realVideoName},{fakeVideoName},{totalFrames},{totalTiles},{runtimeRPrime},{runtimeFPrime},{len(mismatchRPrime)},{len(matchingRPrime)},{len(mismatchFPrime)},{len(matchingFPrime)}\n")

    f.close()

