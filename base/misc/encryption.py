from . import AESEnc as AES

aes = AES.AESCipher("Vegetation")

def encrypt(password):
    return aes.encrypt(password)

def decrypt(encrypted_password):
    return aes.decrypt(encrypted_password)