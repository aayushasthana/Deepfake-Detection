import sys

import rsa

def Gen_key():
    (public_key, private_key) = rsa.newkeys(224)
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

def embedSignatureInTile(tile, signature):

    arr = [[0 for x in range(TILE_SIZE)] for y in range(TILE_SIZE)]

    ''' 
    print("\n ---Sign---\n")
    for i in range(0, 28):
        print("[" + format(sign[i], '08b') + "]", end="")
    print("\n ---Sign---\n")
    '''
    k = 0
    mask = 3 # 0x00000011  to extract 2 bits
    count = 1
    # print("[r][c]  Arr     |  Sign       &    Mask   =  updated Arr ")
    for r in range(0, TILE_SIZE):
        for c in range(0, m):
            if (r == 0) or (c == 0) or (r == TILE_SIZE - 1) or (c == TILE_SIZE - 1):
                '''
                print("[{}][{}]".format(r, c), end=" ")
                print(format(arr[r][c], '08b') + " | ", end=" ")
                print(format(sign[k], '08b') + "[" + str(k) + "]" + " & ", end=" ")
                print(format(mask, '08b') + " = ", end=" ")
                '''
                arr[r][c] |= sign[k] & mask
                print(format(arr[r][c], '08b'))
                if count == 4:
                    k += 1
                    count = 1
                    mask = 3
                else:
                    count += 1
                    mask = mask << 2
    print("\n--sign count {}".format(k))






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
    for i in range(0, 8):
        for j in range(0, 8):
            print("["+format(arr[i][j], '08b')+"]", end="")
            print(format(arr[i][j], '08b'), end=" ")
        print("\n")
    
    For a  m x m 2D matrix
    k = 0
    for r in range(0,m):
        for c in range(0,m): 
         if (r == 0) or (c == 0) or (r == m-1) or (c == m-1)
            tile[r,c] |= sign[k] & (mask <<  (2*count) )
            
            if (count == 4 ) :
                k += 1
                count = 1
            else :
                count += 1
            
    tile[0,0] &= sign[0] & b'11'
    tile[0,1] &= sign[0] & b'1100'
    tile[0,2] &= sign[0] & b'110000'
    tile[0,3] &= sign[0] & b'11000000'
    
    tile[0,4] &= sign[1] & b'11'
    tile[0,5] &= sign[1] & b'1100'
    tile[0,6] &= sign[1] & b'110000'
    tile[0,7] &= sign[1] & b'11000000'
    
    tile[1,7] &= sign[2] & b'11'
    tile[2,7] &= sign[2] & b'1100'
    tile[3,7] &= sign[2] & b'110000'
    tile[4,7] &= sign[2] & b'11000000'
    
    tile[5,7] &= sign[3] & b'11'
    tile[6,7] &= sign[3] & b'1100'
    tile[7,7] &= sign[3] & b'110000'
    tile[7,6] &= sign[3] & b'11000000'
    
    tile[7,5] &= sign[4] & b'11'
    tile[7,4] &= sign[4] & b'1100'
    tile[7,3] &= sign[4] & b'110000'
    tile[7,2] &= sign[4] & b'11000000'
    
    tile[7,1] &= sign[5] & b'11'
    tile[7,0] &= sign[5] & b'1100'
    tile[6,0] &= sign[5] & b'110000'
    tile[5,0] &= sign[5] & b'11000000'
    
    tile[4,0] &= sign[6] & b'11'
    tile[3,0] &= sign[6] & b'1100'
    tile[2,0] &= sign[6] & b'110000'
    tile[1,0] &= sign[6] & b'11000000'
    
    
    
    '''

