from Crypto.Cipher import AES
from Crypto.Random import new as Random
from hashlib import sha256
from base64 import b64encode,b64decode
from django.conf import settings
import hashlib

class AESCipher:
  def __init__(self,key):
    self.block_size = 16
    self.key = sha256(key.encode()).digest()[:32]
    self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr (self.block_size - len(s) % self.block_size)
    self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

  def encrypt(self, data):
    plain_text = self.pad(data)
    iv = Random().read(AES.block_size)
    cipher = AES.new(self.key,AES.MODE_OFB,iv)
    return b64encode(iv + cipher.encrypt(plain_text.encode())).decode()

  def decrypt(self, data):
    cipher_text = b64decode(data.encode())
    iv = cipher_text[:self.block_size]
    cipher = AES.new(self.key,AES.MODE_OFB,iv)
    return self.unpad(cipher.decrypt(cipher_text[self.block_size:])).decode()


def hash_email(data):
  return hashlib.md5(
          hashlib.sha256(
            hashlib.md5(
              str.encode(settings.SECRET_KEY)
              ).digest()+
            hashlib.sha1(
              str.encode(data)
              ).digest()
            ).digest()
          ).hexdigest()

def hash_email_verify(data, hash):
  return hashlib.md5(
          hashlib.sha256(
            hashlib.md5(
              str.encode(settings.SECRET_KEY)
              ).digest()+
            hashlib.sha1(
              str.encode(data)
              ).digest()
            ).digest()
          ).hexdigest() == hash