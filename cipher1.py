import base64
import hashlib
from Crypto.Cipher import AES


BS = 16
pad = (lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode())
unpad = (lambda s: s[:-ord(s[len(s)-1:])])


class AESCipher(object):
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, message):
        message = message.encode()
        raw = pad(message)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf-8'))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf-8'))
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')

    def __iv(self):
        return chr(0) * 16


key = 'secretkey'
message = '테스트'
  
aes = AESCipher(key)
encrypt = aes.encrypt(message)
decrypt = aes.decrypt(encrypt)
  
print(encrypt)
print(decrypt)



#### 양방향 암호화 #####
# 1. pip 설치
# 2. python 설치(현재 3.9.x)
# 3. cmd에서 이 프로젝트 폴더로 이동해서 아래 명령어 실시 ( python 3.x window의 경우 pycryptodome 을 설치해야함)
# pip install pycryptodome

# 실행
# 코드입력 후, Ctrl + F5 
