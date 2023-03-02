
import rsa
from globals import *

def Gen_key():
    (public_key, private_key) = rsa.newkeys(KEYBYTES*8)
    with open(
        r"publicKey.pem", "wb"
    ) as key:
        key.write(public_key.save_pkcs1("PEM"))
    with open(
        r"privateKey.pem", "wb"
    ) as key:
        key.write(private_key.save_pkcs1("PEM"))

def get_keys():
    with open(
        r"publicKey.pem", "rb"
    ) as key:
        publicKey = rsa.PublicKey.load_pkcs1(key.read())
    with open(
        r"privateKey.pem", "rb"
    ) as key:
        privateKey = rsa.PrivateKey.load_pkcs1(key.read())
    return publicKey,privateKey

def asymmetric_encrypt(data, publicKey):
    encrypt_data = rsa.encrypt(data.encode(), publicKey)
    return encrypt_data


def asymmetric_decrypt(encrypted_data, privateKey):
    decrypted_data = rsa.decrypt(encrypted_data, privateKey).decode()
    return decrypted_data



'''
Delete this test code
if __name__ == '__main__':
    #Gen_key()
    publicKey, privateKey = get_keys()
    signature = "13115716408288401"
    enrypted_signature = rsa.encrypt(signature.encode(), publicKey)
    print("ES:Len {} {}".format(len(enrypted_signature),enrypted_signature))

    for i in range(0,27):
        print(format(enrypted_signature[i],'08b'), end=" ")
    print("\n-----\n")
    sign = enrypted_signature

    rows =8
    cols =8
    arr = [[0 for x in range(rows)] for y in range(cols)]

    print("\n ---Sign---\n")
    for i in range(0, 28):
            print("[" + format(sign[i], '08b') + "]", end="")
    print("\n ---Sign---\n")

    k = 0
    m = 8
    mask = 3

    count = 1
    print("[r][c]  Arr     |  Sign       &    Mask   =  updated Arr ")
    for r in range(0, m):
        for c in range(0, m):
            if (r == 0) or (c == 0) or (r == m - 1) or (c == m - 1):
                print("[{}][{}]".format(r,c),end=" ")
                print(format(arr[r][c], '08b')+" | ", end = " ")
                print(format(sign[k], '08b') + "["+str(k)+ "]"+ " & ", end=" ")
                print(format(mask, '08b')+ " = ",end=" ")

                arr[r][c] |= sign[k] & mask
                print(format(arr[r][c], '08b'))
                if (count == 4):
                    k += 1
                    count = 1
                    mask = 3
                else:
                    count += 1
                    mask = mask << 2
    print("\n--sign count {}".format(k))
'''