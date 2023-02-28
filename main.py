import copy
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np
import rsa
import json
import argparse
import tqdm
from tqdm import tqdm
from collections import Counter


# Globals
TILE_SIZE = 48
BASE_PATH = "/Users/aayushasthana/DeepfakeProject/"
DATA_PATH = "dfdc-data/"
FILE_PATH = "dfdc_train_part_0/"

METADATA_NAME = "metadata.json"

def cli_options():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--count", required=False,
                    help="count of videos")
    ap.add_argument("-j", "--json", required=False,
                    help="json meta data file path")

    args = vars(ap.parse_args())

    return args


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
            count+=1


    f.close()
    print(dict_videos)
    return count ,dict_videos

def read_video(video_name,frames):

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
    frames_array = np.array(frames)
    cap.release()
    return count, width, height, fps, frames_array


def display_tile(frames, frame_number, row, col, title):
    plt.imshow(frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])
    plt.title(title + "-f#{} r#{} c#{}".format(frame_number, row, col))
    plt.show()

def add_tile_border(frames, frame_number, row, col):
    tile = frames[frame_number][row:row+TILE_SIZE,col:col+TILE_SIZE]

    tile[0:5, :, 0] = 0
    tile[0:5, :, 1] = 0
    tile[0:5, :, 2] = 255

    tile[TILE_SIZE - 5:TILE_SIZE, :, 0] = 0
    tile[TILE_SIZE - 5:TILE_SIZE, :, 1] = 0
    tile[TILE_SIZE - 5:TILE_SIZE, :, 2] = 255

    tile[:, 0:5, 0] = 0
    tile[:, 0:5, 1] = 0
    tile[:, 0:5, 2] = 255

    tile[:,TILE_SIZE - 5:TILE_SIZE,0] = 0
    tile[:,TILE_SIZE - 5:TILE_SIZE,1] = 0
    tile[:,TILE_SIZE - 5:TILE_SIZE,2] = 255


def dump_tile(frames, frame_number, row, col, title):
    print(title + "-f#{} r#{} c#{}".format(frame_number, row, col))
    print(frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])


def Avg_tile(frames, frame_number, row, col):
    tile = np.array(frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])
    R = tile[:, :, 0]
    R46 = R[1:-1, 1:-1]

    G = tile[:, :, 1]
    G46 = G[1:-1, 1:-1]

    B = tile[:, :, 2]
    B46 = B[1:-1, 1:-1]

    return int(np.average(R46)), int(np.average(G46)), int(np.average(B46))


def display_frame(frames, frame_number, title):
    plt.figure()
    plt.imshow(cv2.cvtColor(frames[frame_number], cv2.COLOR_BGR2RGB))
    plt.title(title + "-f#{}".format(frame_number))
    plt.show()


def create_signature(avgR, avgG, avgB, frame_number, row, col):
    data_string = str(avgR) + str(avgG) + str(avgB) + str(frame_number) + str(row * col)
    return data_string


def asymmetric_encrypt(data, publicKey):
    encrypt_data = rsa.encrypt(data.encode(), publicKey)
    return encrypt_data


def asymmetric_decrypt(encrypted_data, privateKey):
    decrypted_data = rsa.decrypt(encrypted_data, privateKey).decode()
    return decrypted_data


def get_keys():
    with open(
            r"publicKey.pem", "rb"
    ) as key:
        publicKey = rsa.PublicKey.load_pkcs1(key.read())
    with open(
            r"privateKey.pem", "rb"
    ) as key:
        privateKey = rsa.PrivateKey.load_pkcs1(key.read())
    return publicKey, privateKey

#Embedding
def embedSignatureInTile(tile, signature):
    mask1 = [224, 28, 3]
    mask2 = [31, 227, 252]
    # mask = [b'11100000', b'00011100', b'00000011']
    # mask2 = [b'00011111', b'11100011', b'11111100']

    for color in range(0, 3):
        transfer = np.bitwise_and(signature, mask1[color])
        transfer2 = np.bitwise_and(tile[0, 8:40, color], mask2[color])
        tile[0, 8:40, color] = np.bitwise_or(transfer2, transfer)

    return tile



def extractSignature(tile):
    extracted_signature = np.array(bytearray(32))
    mask = [224, 28, 3]

    for color in range(0, 3):
        transfer = np.bitwise_and(tile[0, 8:40, color], mask[color])
        extracted_signature = np.bitwise_or(extracted_signature, transfer)

    return extracted_signature


def CompareRealandFake(r_frames,real_h, real_w,real_frame_count,f_frames,fake_h,fake_w,fake_frame_count):

    # Check various metadata parameters
    # for now assume they are the same
    print_hash_count = int(len(r_frames)*(real_h/TILE_SIZE)*(real_w/TILE_SIZE))
    progress_bar = tqdm(desc="Compare Signatures", total=print_hash_count)
    publicKey, privateKey = get_keys()
    matching = []
    mismatch = []
    match_dict = {}
    mistmatch_dict ={}
    for frame_number in range(0, len(r_frames)):
        for row in range(0, real_h, TILE_SIZE):
            for col in range(0, real_w, TILE_SIZE):
                real_currTile = np.array(r_frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])

                # Extracting the signature from real video

                extractedSignature = extractSignature(real_currTile)
                decryptedSignature = asymmetric_decrypt(extractedSignature, privateKey)

                # Calculate Signature from Fake
                fake_currTile = np.array(f_frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])

                AvgR, AvgG, AvgB = Avg_tile(f_frames, frame_number, row, col)
                signature = create_signature(AvgR, AvgG, AvgB, frame_number, row, col)

                if (decryptedSignature == signature ):
                    matching.append((row,col))
                    #match_dict[str(row)+"-"+str(col)] += 1
                else:
                    mismatch.append((row,col))
                    #mistmatch_dict[str(row)+"-"+str(col)] += 1
                progress_bar.update(1)
    return matching, mismatch, match_dict, mistmatch_dict


def EmbeddSignature(video_name, frames,h,w):

    print_hash_count = int(len(frames)*(h/TILE_SIZE)*(w/TILE_SIZE))
    progress_bar = tqdm(desc="Embed Signature", total=print_hash_count)
    # Encrypting the signature
    publicKey, privateKey = get_keys()

    for frame_number in range(0, len(frames)):
        for row in range(0, h, TILE_SIZE):
            for col in range(0, w, TILE_SIZE):

                # Signature creation
                AvgR, AvgG, AvgB = Avg_tile(frames, frame_number, row, col)
                signature = create_signature(AvgR, AvgG, AvgB, frame_number, row, col)

                # Encrypting the signature
                publicKey, privateKey = get_keys()
                encryptedSignature = asymmetric_encrypt(signature, publicKey)

                # Embedding the signature
                #currTile = np.array(frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])
                encryptedSignature = np.array(list(encryptedSignature), dtype=int).reshape(32)
                currTile = np.array(embedSignatureInTile(frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE], encryptedSignature))

                # Extracting the signature
                #extractedSignature = extractSignature(frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])
                #decryptedSignature = asymmetric_decrypt(extractedSignature, privateKey)

                progress_bar.update(1)


    return np.array(frames)



if __name__ == '__main__':

    args = cli_options()
    video_count = args["count"]
    json_file = args["json"]

    print(video_count, json_file)


    metadata_count, metadata_dict = getMetadata(json_file)

    fake_video_name = metadata_dict[int(video_count)][0]
    real_video_name = metadata_dict[int(video_count)][1]
    real_video_name_path = BASE_PATH + DATA_PATH + FILE_PATH + real_video_name
    fake_video_name_path = BASE_PATH + DATA_PATH + FILE_PATH + fake_video_name
    frames = []

    real_frame_count, real_w, real_h, real_fps, real_frames = read_video(real_video_name_path,frames)

    print(f"REAL:{real_video_name}--FC:{real_frame_count}, Width:{real_w}, Height:{real_h}, FPS:{real_fps}")
    # leave out partial tiles

    real_h = real_h - real_h % TILE_SIZE
    real_w = real_w - real_w % TILE_SIZE

    print( real_h, real_w )

    real_frames = EmbeddSignature(real_video_name,real_frames,real_h,real_w)

    f_frames = []
    fake_frame_count, fake_w, fake_h, fake_fps, fake_frames = read_video(fake_video_name_path,f_frames)
    print(f"FAKE:{fake_video_name} -FC:{fake_frame_count}, Width:{fake_w}, Height:{fake_h}, FPS:{real_fps}")
    # leave out partial tiles
    fake_h = fake_h - fake_h % TILE_SIZE
    fake_w = fake_w - fake_w % TILE_SIZE

    total_tiles = fake_frame_count * (fake_h/TILE_SIZE) * (fake_w /TILE_SIZE)
    matching , mismatch, match_dict, mismatch_dict = CompareRealandFake(real_frames,real_h, real_w,real_frame_count,fake_frames,fake_h,fake_w,fake_frame_count)

    match_counter = Counter(matching)
    mismatch_counter= Counter(matching)
    mismatch_counter.most_common(10)

    tiles_per_frame = (fake_h/TILE_SIZE) * (fake_w /TILE_SIZE)
    top_25_onFrame = int(0.25 * tiles_per_frame)
    top_50_onFrame = int(0.5 * tiles_per_frame)
    top_25 = dict((k, v) for k, v in mismatch_counter.items() if v >= 0.75 * fake_frame_count)
    top_50 = dict((k, v) for k, v in mismatch_counter.items() if v >= 0.50 * fake_frame_count)
    print(f" Tile  that change in 75% of frames {top_25}")
    print(f" Tile  that change in 50% of frames {top_50}")

    print(f" Top 25% changed tiles {mismatch_counter.most_common(75)}")
    print(f" Top 50% changed tiles {mismatch_counter.most_common(150)}")
    l = mismatch_counter.most_common(top_50_onFrame)

    for f in range(0,fake_frame_count):
        for t in l:
            add_tile_border(fake_frames,f,t[0][0],t[0][1])


    print(f" Total Matching {float(len(matching) / total_tiles) * 100} Total mismatch  {float(len(mismatch) / total_tiles) * 100}")



    while True:
        for f in range(0,fake_frame_count):
            cv2.imshow('fake bordered', fake_frames[f])
            cv2.imshow('original', real_frames[f])
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.waitKey(0)



