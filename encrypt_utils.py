import hashlib
import rsa


def asymmetric_encrypt(data, publicKey):
    enrypt_data = rsa.encrypt(data.encode(), publicKey)
    return enrypt_data


def asymmetric_decrypt(encrypted_data, privateKey):
    decrypted_data = rsa.decrypt(encrypted_data, privateKey).decode()
    return decrypted_data



def Gen_keys():
    (public_key, private_key) = rsa.newkeys(224)
    with open(
        r"publicKey.pem", "wb"
    ) as key:
        key.write(public_key.save_pkcs1("PEM"))
    with open(
        r"privateKey.pem", "wb"
    ) as key:
        key.write(private_key.save_pkcs1("PEM"))

def Get_keys():
    with open(
            r"publicKey.pem", "rb"
    ) as key:
        publicKey = rsa.PublicKey.load_pkcs1(key.read())
    with open(
            r"privateKey.pem", "rb"
    ) as key:
        privateKey = rsa.PrivateKey.load_pkcs1(key.read())
    return publicKey, privateKey

