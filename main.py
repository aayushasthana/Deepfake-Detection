import time
import cv2
import matplotlib.pyplot as plt
import numpy as np
import rsa

# Globals
TILE_SIZE = 48

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


if __name__ == '__main__':
    videos = ["man_face.mp4", "woman_face.mp4"]
    frame_count, w, h, fps, frames = read_video(videos[0])
    print("Framecount: {}, Width: {}, Height: {}, FPS: {}\n".format(frame_count, w, h, fps))

    startTime = time.time()
    for frame_number in range(0, len(frames)):
        prev = time.time()
        for row in range(0, h, TILE_SIZE):
            for col in range(0, w, TILE_SIZE):
                # Signature creation
                AvgR, AvgG, AvgB = Avg_tile(frames, frame_number, row, col)
                signature = create_signature(AvgR, AvgG, AvgB, frame_number, row, col)

                # Encrypting the signature
                publicKey, privateKey = get_keys()
                encryptedSignature = asymmetric_encrypt(signature, publicKey)

                # Embedding the signature
                currTile = np.array(frames[frame_number][row:row + TILE_SIZE, col:col + TILE_SIZE])
                encryptedSignature = np.array(list(encryptedSignature), dtype=int).reshape(32)
                currTile = np.array(embedSignatureInTile(currTile, encryptedSignature))

                # Extracting the signature
                extractedSignature = extractSignature(currTile)
                decryptedSignature = asymmetric_decrypt(extractedSignature, privateKey)

        print(f"Frame Number: {frame_number+1}, Total Time: {time.time()-startTime}, Split: {time.time()-prev}")

    endTime = time.time()
    print(endTime - startTime)
