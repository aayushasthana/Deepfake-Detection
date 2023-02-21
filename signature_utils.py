# This is a sample Python script.
import numpy as np
from encrypt_utils import *

TILE_SIZE = 8


def Avg_tile(frames, frame_number, row, col):
    tile = np.array(frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])
    # print(tile.shape)
    R = tile[:, :, 0]
    R6 = R[1:-1, 1:-1]

    G = tile[:, :, 1]
    G6 = G[1:-1, 1:-1]

    B = tile[:, :, 2]
    B6 = B[1:-1, 1:-1]

    return int(np.average(R6)), int(np.average(G6)), int(np.average(B6))


'''
This function creates a signature of a tile based on mean value of the pixels in the tile
It will ignore the border pixels

'''


def create_signature_Avg(frames, frame_number, row, col):
    avgR, avgG, avgB = Avg_tile(frames, frame_number, row, col)
    data_string = str(avgR) + str(avgG) + str(avgB) + str(frame_number) + str(row * col)

    return data_string


'''
tile :2D list
sign = signature
k = signature byte number
 Each time this function is called - k advances by 7 bytes
 total border pixels = 28
 total bits embedded = 28 x 2 = 56 bits = 7 bytes

'''


def embed_2BitsBorder(tile, sign, k, dbg_str):
    mask = 3  # 0x00000011  to extract 2 bits
    not_mask = ~mask
    shift_value = 2
    count = 0

    for r in range(0, TILE_SIZE):
        for c in range(0, TILE_SIZE):
            if (r == 0) or (c == 0) or (r == TILE_SIZE - 1) or (c == TILE_SIZE - 1):

                new_mask = mask << (shift_value * count)
                bits_extract = sign[k] & new_mask
                bits_extract = bits_extract >> (shift_value * count)
                tile[r][c] &= not_mask
                tile[r][c] |= bits_extract

                if count == 3:
                    k += 1
                    count = 0
                    new_mask = 0
                else:
                    count += 1

    return k


'''
The code is very much similar to the above - the ony difference is the mask  and the shift_value
May be these could be passed as a param
This function needs to be tested
'''


def embed_1BitBorder(tile, sign, k, marker, dbg_str):
    mask = 1  # 0x00000001  to extract 1 bit

    shift_value = 1
    count = marker

    for r in range(0, TILE_SIZE):
        for c in range(0, TILE_SIZE):
            if (r == 0) or (c == 0) or (r == TILE_SIZE - 1) or (c == TILE_SIZE - 1):
                mask = mask << (shift_value * count)
                res = sign[k] & mask
                res = res >> (shift_value * count)

                if (res == 1):
                    tile[r][c] |= 4
                else:
                    tile[r][c] &= ~4

                if count == 7:
                    k += 1
                    count = 0
                    mask = 1
                else:
                    count += 1
                    mask = 1
    return k


def embedSignatureInTile(tile, signature):
    '''
    Calculations:
    1. total bits to hide = signature size x 8 = 28 x 8 = 224 bits
    2. Embed 2 bits for each Red, Green, Blue to the border pixels
       Calculations: total border pixel = (8x8)-(6x6) = 28
       total signature bits hidden = 28 x 3 x 2 = 168 bits
    3. Embed 1 but for each Red, Green, Blue to the border pixels
       Calculations: total additional signature bits hidden
        = 28 x 3 x 1 = 84 bits
    4. Total bits hidden so far = 168 + 84 = 252. This is well within the limit of 224 bits ( Extra space = 252-224 = 28)
    5. So, don't embed all border pixels, so just do it for Green and Blue and drop Red
       New calculations: 28 x 2 x 1 = 56
       Total = 168 + 56 = 224

    :param tile:
    :param signature:
    :return:
    '''
    R = tile[:, :, 0]
    G = tile[:, :, 1]
    B = tile[:, :, 2]
    k = 0
    k = embed_2BitsBorder(R, signature, k, "red")  # Red   k = 0 - 6      7
    k = embed_2BitsBorder(G, signature, k, "green")  # Green k = 7 - 13     7
    k = embed_2BitsBorder(B, signature, k, "blue")  # Blue  k = 14 - 20    7
    k = embed_1BitBorder(G, signature, k, 0, "green-1")  # Green  k = 21 - 23    3
    k = embed_1BitBorder(B, signature, k, 4, "blue-1")  # Blue   k = 24 - 26    3


def extract_2BitsBorder(tile, ret_sign, k):
    mask = 3  # 0x00000011  to extract 2 bits
    shift_value = 2
    count = 0

    for r in range(0, TILE_SIZE):
        for c in range(0, TILE_SIZE):
            if (r == 0) or (c == 0) or (r == TILE_SIZE - 1) or (c == TILE_SIZE - 1):

                ret_sign[k] |= (tile[r][c] & mask) << (shift_value * count)

                if count == 3:
                    k += 1
                    count = 0
                    mask = 3
                else:
                    count += 1
    return k


def extract_1BitBorder(tile, ret_sign, k, marker):
    mask = 1  # 0x00000001  to extract 1 bit
    mask = mask << marker
    shift_value = 1
    count = marker
    bit_count = marker

    for r in range(0, TILE_SIZE):
        for c in range(0, TILE_SIZE):
            if (r == 0) or (c == 0) or (r == TILE_SIZE - 1) or (c == TILE_SIZE - 1):
                ret_sign[k] |= ((tile[r][c] & 4) >> 2) << count
                if count == 7:
                    k += 1
                    count = 0
                    mask = 1
                    bit_count = 0
                else:
                    count += 1

    return k


def extractSignature(tile):
    extracted_signature = [0 for x in range(28)]

    R = tile[:, :, 0]
    G = tile[:, :, 1]
    B = tile[:, :, 2]

    k = 0
    k = extract_2BitsBorder(R, extracted_signature, 0)  # Red   k = 0 - 6
    k = extract_2BitsBorder(G, extracted_signature, k)  # Green k = 7 - 13
    k = extract_2BitsBorder(B, extracted_signature, k)  # Blue  k = 14 - 21
    k = extract_1BitBorder(G, extracted_signature, k, 0)  # Green
    k = extract_1BitBorder(B, extracted_signature, k, 4)  # Blue

    return extracted_signature


'''
This function will calculate the signature from a source_tile
 and embed it in the destination_tile
'''


def AssignSignature_perTile(frames, src_frame_number, src_row, src_col, dest_frame_number, dest_row, dest_col):

    # create signature from the source tile
    signature = create_signature_Avg(frames, src_frame_number, src_row, src_col)
    # Encrypting the signature
    publicKey, privateKey = Get_keys()
    encrypt_signature = asymmetric_encrypt(signature, publicKey)

    # Embed the signature in destination tile
    t = np.array(frames[dest_frame_number][dest_row:dest_row + TILE_SIZE, dest_col:dest_col + TILE_SIZE])
    embedSignatureInTile(t, encrypt_signature)



def AssignSignature_ListofTile(frames,src_frame_number, src_tile_list, dest_frame_number, dest_tile_list):

    for i in range(0, len(src_tile_list)) :
        (src_row, src_col)   = src_tile_list[i]
        (dest_row, dest_col) = dest_tile_list[i]
        AssignSignature_perTile(frames, src_frame_number, src_row, src_col, dest_frame_number, dest_row, dest_col)



