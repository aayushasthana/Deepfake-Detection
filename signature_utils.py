import numpy as np
import tqdm
from tqdm import tqdm
from globals import *
from encrypt_utils import *


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


def createSignature(avgR, avgG, avgB, frame_number, row, col):
    data_string = str(avgR) + str(avgG) + str(avgB) + str(frame_number) + str(row * col)
    return data_string


# Embedding
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


def compareSignature(framesA, decryptA, framesB, decryptB, h, w, count, publicKey, privateKey):
    # Check various metadata parameters
    # for now assume they are the same
    tqdm_value = count * int((h / TILE_SIZE) * (w / TILE_SIZE))
    progress_bar = tqdm(desc="Compare Signatures", total=tqdm_value)

    matching = []
    mismatch = []

    for f in range(0, count):
        for row in range(0, h, TILE_SIZE):
            for col in range(0, w, TILE_SIZE):
                tileA = np.array(framesA[f][row:row + TILE_SIZE, col:col + TILE_SIZE])
                tileB = np.array(framesB[f][row:row + TILE_SIZE, col:col + TILE_SIZE])

                # Extracting the signature
                if decryptA:
                    try:
                        extractedSignatureA = extractSignature(tileA)
                        signatureA = asymmetric_decrypt(extractedSignatureA, privateKey)

                    except:
                        print(f"A:Decrypt Failed F#{f}:({row},{col})")
                        signatureA = ""
                else:
                    AvgR, AvgG, AvgB = Avg_tile(framesA, f, row, col)
                    signatureA = createSignature(AvgR, AvgG, AvgB, f, row, col)

                if decryptB:
                    try:
                        extractedSignatureB = extractSignature(tileB)
                        signatureB = asymmetric_decrypt(extractedSignatureB, privateKey)
                    except:
                        print(f"B:Decrypt Failed F#{f}:({row},{col})")
                        signatureB = ""
                else:
                    AvgR, AvgG, AvgB = Avg_tile(framesB, f, row, col)
                    signatureB = createSignature(AvgR, AvgG, AvgB, f, row, col)

                if signatureA == signatureB:
                    matching.append((row, col))
                else:
                    mismatch.append((row, col))
                    #print(f"A: {signatureA} & B: {signatureB}")
                progress_bar.update(1)

    return matching, mismatch


def embedSignature(frames, h, w, count, publicKey, privateKey):
    tqdm_value = count * int((h / TILE_SIZE) * (w / TILE_SIZE))
    progress_bar = tqdm(desc="Embed Signature   ", total=tqdm_value)

    for f in range(0, count):
        for row in range(0, h, TILE_SIZE):
            for col in range(0, w, TILE_SIZE):
                # Signature creation
                AvgR, AvgG, AvgB = Avg_tile(frames, f, row, col)
                signature = createSignature(AvgR, AvgG, AvgB, f, row, col)
                encryptedSignature = asymmetric_encrypt(signature, publicKey)
                encryptedSignature = np.array(list(encryptedSignature), dtype=int).reshape(32)
                currTile = np.array(embedSignatureInTile(frames[f][row:row + TILE_SIZE, col:col + TILE_SIZE],
                                    encryptedSignature))

                progress_bar.update(1)

    return np.array(frames)
