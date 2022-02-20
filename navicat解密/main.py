# -*- coding: utf-8 -*-
from Crypto.Cipher import AES


def DecryptNavicat(data):
    aes = AES.new('libcckeylibcckey'.encode(), AES.MODE_CBC, iv='libcciv libcciv '.encode())
    text = aes.decrypt(bytes.fromhex(data))
    # 删掉填充的字符
    return text[0:-text[-1]].decode('utf-8')


if __name__ == '__main__':
    print(DecryptNavicat('加密的密码'))

