# coding:utf-8
from Crypto.PublicKey.RSA import RsaKey
from Crypto.PublicKey import RSA
from Server.api.RSA_KEY import PRI_KEY,PUB_KEY
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64




def enc(text):
    rsa_key = RSA.importKey(PUB_KEY)

    cipher = Cipher_pkcs1_v1_5.new(rsa_key)

    cipher_text = cipher.encrypt(text.encode('utf-8'))

    return base64.b64encode(cipher_text).decode('utf-8')


def dec(cipher_text):
    cipher_text = base64.b64decode(cipher_text.encode('utf-8'))
    rsa_key = RSA.importKey(PRI_KEY)
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)

    plaintext = cipher.decrypt(cipher_text,b"").decode()
    return plaintext



