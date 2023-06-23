from base64 import b64encode, b64decode
from binascii import unhexlify

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from os import environ


def encrypt_credentials(msg):
    iv = environ.get('encrypt_iv')
    password = environ.get('encrypt_password')
    # Convert Hex String to Binary
    iv = unhexlify(iv)
    password = unhexlify(password)

    # Pad to AES Block Size
    msg = pad(msg.encode(), AES.block_size)

    # Encipher Text
    cipher = AES.new(password, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(msg)

    # Encode Cipher_text as Base 64 and decode to String
    out = b64encode(cipher_text).decode('utf-8')
    return out
    # print(f"OUT: {out}")

    # Decipher cipher text
    decipher = AES.new(password, AES.MODE_CBC, iv)
    # UnPad Based on AES Block Size
    plaintext = unpad(decipher.decrypt(b64decode(out)), AES.block_size).decode('utf-8')
    # print(f'PT: {plaintext}')


def decrypt_credentials(msg):
    iv = environ.get('encrypt_iv')
    password = environ.get('encrypt_password')
    iv = unhexlify(iv)
    password = unhexlify(password)
    decipher = AES.new(password, AES.MODE_CBC, iv)
    plaintext = unpad(decipher.decrypt(b64decode(msg)), AES.block_size).decode('utf-8')
    return plaintext
