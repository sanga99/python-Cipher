# python-Cipher
[python] 단방향 암호화 / 양방향 암호화 / 복호화 / AWS S3 buket

    1. pip 설치
    2. python 설치(현재 3.9.x)
    3. cmd에서 이 프로젝트 폴더로 이동해서 아래 명령어 실시 ( python 3.x window의 경우 pycryptodome 을 설치해야함)
        pip install pycryptodome
        
<br/>

###### gen_sha256_hashed_key_salt : 

    암호화한 key에서 더욱이 보안강화를 위해 salt(소금)을 치는 것처럼 처리
    암호화만 하면, 암호화한 key만 알면 그 키를 그대로 복호화 했을때 찾아낼수 있으므로
