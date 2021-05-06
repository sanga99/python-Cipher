
##############################################################################################################
#######################양방향암호화,복호화, 단방향암호화, key는 s3 버킷에 올림###################################
#######################코드 아래 다른 버전도 있음###############################################################

# 만약 HASH_KEY 관련 Error가 난다면, S3에서 public(url접근권한)이 설정이 안되어 있을 가능성이 크다
# create_presigned_url메소드에서 생성되는 url이 잘 접속이 되는지 링크들어가 먼저 확인해 보기 
# 링크 접속 시 정상값 : {'HASH_KEY': 'AESUserKey', 'HASH_IV': 'AESEncIv'}

import copy
import boto3
import base64
import hashlib
import requests
from Cryptodome import Random
from Cryptodome.Cipher import AES

class Cipher:
    def __init__(self):
        key_list = self.get_cipher_key()
        self.key = self.gen_sha256_hashed_key_salt(key_list['HASH_KEY'])
        iv = self.gen_sha256_hashed_key_salt(key_list['HASH_IV'])
        self.iv = iv[:16]
        
    # 암호화한 key에서 더욱이 보안강화를 위해 salt(소금)을 치는 것처럼 처리
    # 암호화만 하면, 암호화한 key만 알면 그 키를 그대로 복호화 했을때 찾아낼수 있으므로
    def gen_sha256_hashed_key_salt(self, key):
    	utf8Key = key.encode('utf-8')
    	salt1 = hashlib.sha256(utf8Key).digest()
    	return hashlib.sha256(salt1+utf8Key).digest()
    
    def get_cipher_key(self):
        url = self.create_presigned_url()
        response = requests.get(url)
        data = []
        list = {}
        for res in response:
            data = res.decode('utf-8').split()
        for key in data:
            keyval = key.split('=')
            list.update({keyval[0]:keyval[1]})
        
        return list

    # s3에 지정 buket에 url 생성
    def create_presigned_url(self, expiration=20):
        s3_client = boto3.client('s3')
        BUCKET_NAME = '***'
        KEY = 'key.txt'
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': BUCKET_NAME, 'Key': KEY},
                                                    ExpiresIn=3000)
                                                    # ExpiresIn=expiration)
        return response

    	
    # 양방향 복호화
    def AES256Decrypt(self, cipher):
        cip = cipher
        cipherType = str( type(cipher) )
        if(cipherType!="<class 'str'>"):
            cip = cipher.value
            
        encryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
        plain = encryptor.decrypt(cip)
        plain = plain[0:-plain[-1]]
        plain = plain.decode('utf-8')
        return plain
    

    # 양방향 암호화
    def AES256Encrypt(self, plain):
    	length = AES.block_size - (len(plain) % AES.block_size)
    	plain += chr(length)*length
    	thePlain = plain.encode('utf-8')
    	
    	encryptor = AES.new(self.key, AES.MODE_CBC, self.iv)
    	return encryptor.encrypt(thePlain)


    # 단방향 암호화
    def encodeSHA(self, password):
        encodePw = password.encode('utf-8')
        hashSHA = hashlib.sha256()
        hashSHA.update(encodePw)
        
        hexPw = hashSHA.hexdigest()
        result = hexPw.upper()
        return result


# TEST 해보기
msg = 'namenamename'

obj = Cipher()
encData = obj.AES256Encrypt(msg)
print(encData)



###################################################################################################
#######################아래는 양방향 암호화만 처리 (chiper1.py파일 내용)##############################


# import base64
# import hashlib
# # 1)
# # from Crypto.Cipher import AES         
# # 2) 
# from Cryptodome import Random
# from Cryptodome.Cipher import AES
# # 1), 2) 모두 됨(결과동일)


# BS = 16
# pad = (lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode())
# unpad = (lambda s: s[:-ord(s[len(s)-1:])])


# class AESCipher(object):
#     def __init__(self, key):
#         self.key = hashlib.sha256(key.encode()).digest()

#     def encrypt(self, message):
#         message = message.encode()
#         raw = pad(message)
#         cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf-8'))
#         enc = cipher.encrypt(raw)
#         return base64.b64encode(enc).decode('utf-8')

#     def decrypt(self, enc):
#         enc = base64.b64decode(enc)
#         cipher = AES.new(self.key, AES.MODE_CBC, self.__iv().encode('utf-8'))
#         dec = cipher.decrypt(enc)
#         return unpad(dec).decode('utf-8')

#     def __iv(self):
#         return chr(0) * 16


# key = 'secretkey'
# message = '테스트'
  
# aes = AESCipher(key)
# encrypt = aes.encrypt(message)
# decrypt = aes.decrypt(encrypt)
  
# print(encrypt)
# print(decrypt)

# #### 양방향 암호화 #####
# # 1. pip 설치
# # 2. python 설치(현재 3.9.x)
# # 3. cmd에서 이 프로젝트 폴더로 이동해서 아래 명령어 실시 ( python 3.x window의 경우 pycryptodome 을 설치해야함)
# # pip install pycryptodome

# # 실행
# # 코드입력 후, Ctrl + F5 
